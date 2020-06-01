pragma solidity >=0.5.0 <0.7.0;
pragma experimental ABIEncoderV2;


contract Data {
    mapping(address => mapping(string => string)) Data_users;

    function save_data(string memory data, string memory index) public {
        address public_key = msg.sender;
        Data_users[public_key][index] = data;
    }

    function fetch_data(address public_key, string memory index) public view returns (string memory){
        return Data_users[public_key][index];
    }

}
