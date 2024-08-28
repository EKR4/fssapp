import streamlit as st
from web3 import Web3
import solcx

# Install the Solidity compiler
solcx.install_solc('0.8.0')

# Connect to Celo blockchain
celo_rpc_url = "https://alfajores-forno.celo-testnet.org"
web3 = Web3(Web3.HTTPProvider(celo_rpc_url))

# Check if connected to the blockchain
if web3.is_connected():
    st.success("Connected to Celo blockchain")
else:
    st.error("Failed to connect to Celo blockchain")

# Smart contract code
contract_code = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FundraisingPlatform {
    struct Campaign {
        address payable creator;
        uint goal;
        uint deadline;
        uint fundsRaised;
        bool completed;
    }

    mapping(uint => Campaign) public campaigns;
    uint public campaignCount;

    event CampaignCreated(uint campaignId, address creator, uint goal, uint deadline);
    event ContributionMade(uint campaignId, address contributor, uint amount);
    event FundsWithdrawn(uint campaignId, address creator, uint amount);

    function createCampaign(uint _goal, uint _duration) public {
        require(_goal > 0, "Goal must be greater than 0");
        require(_duration > 0, "Duration must be greater than 0");

        campaignCount++;
        campaigns[campaignCount] = Campaign({
            creator: payable(msg.sender),
            goal: _goal,
            deadline: block.timestamp + _duration,
            fundsRaised: 0,
            completed: false
        });

        emit CampaignCreated(campaignCount, msg.sender, _goal, block.timestamp + _duration);
    }

    function contribute(uint _campaignId) public payable {
        Campaign storage campaign = campaigns[_campaignId];
        require(block.timestamp < campaign.deadline, "Campaign has ended");
        require(!campaign.completed, "Campaign is already completed");

        campaign.fundsRaised += msg.value;
        emit ContributionMade(_campaignId, msg.sender, msg.value);

        if (campaign.fundsRaised >= campaign.goal) {
            campaign.completed = true;
        }
    }

    function withdrawFunds(uint _campaignId) public {
        Campaign storage campaign = campaigns[_campaignId];
        require(msg.sender == campaign.creator, "Only the creator can withdraw funds");
        require(campaign.completed, "Campaign is not completed yet");

        uint amount = campaign.fundsRaised;
        campaign.fundsRaised = 0;
        campaign.creator.transfer(amount);

        emit FundsWithdrawn(_campaignId, campaign.creator, amount);
    }
}
'''

# Compile the smart contract
compiled_sol = solcx.compile_source(contract_code, output_values=['abi', 'bin'])
contract_interface = compiled_sol['<stdin>:FundraisingPlatform']

# Deploy the smart contract
def deploy_contract():
    account = web3.eth.accounts[0]
    FundraisingPlatform = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = FundraisingPlatform.constructor().transact({'from': account})
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    st.success(f"Contract deployed at address: {contract_address}")
    return contract_address

# Streamlit app
st.title("Celo Fundraising Platform")

if st.button("Deploy Contract"):
    contract_address = deploy_contract()
    st.write(f"Contract Address: {contract_address}")

# Interact with the deployed contract
contract_address = st.text_input("Enter Contract Address")
if contract_address:
    FundraisingPlatform = web3.eth.contract(address=contract_address, abi=contract_interface['abi'])

    st.subheader("Create Campaign")
    goal = st.number_input("Goal (in wei)", min_value=1)
    duration = st.number_input("Duration (in seconds)", min_value=1)
    if st.button("Create Campaign"):
        tx_hash = FundraisingPlatform.functions.createCampaign(goal, duration).transact({'from': web3.eth.accounts[0]})
        web3.eth.waitForTransactionReceipt(tx_hash)
        st.success("Campaign created successfully")

    st.subheader("Contribute to Campaign")
    campaign_id = st.number_input("Campaign ID", min_value=1)
    amount = st.number_input("Amount (in wei)", min_value=1)
    if st.button("Contribute"):
        tx_hash = FundraisingPlatform.functions.contribute(campaign_id).transact({'from': web3.eth.accounts[0], 'value': amount})
        web3.eth.waitForTransactionReceipt(tx_hash)
        st.success("Contribution made successfully")

    st.subheader("Withdraw Funds")
    if st.button("Withdraw Funds"):
        tx_hash = FundraisingPlatform.functions.withdrawFunds(campaign_id).transact({'from': web3.eth.accounts[0]})
        web3.eth.waitForTransactionReceipt(tx_hash)
        st.success("Funds withdrawn successfully")
