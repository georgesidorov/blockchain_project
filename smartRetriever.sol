//SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.7.0;


//  Name: George Sidorov
//  Student number: 15375551
//  Please consult README.md before use.

contract smartRetriever {
    struct Input {
        uint256 index; //  Index is used to record the position of key in keyList.
        bytes value; //  Dynamically-sized byte array for storing SHA512 hash value.
    }
    mapping(bytes16 => Input) map_hashed; //  Declare mapping, Solidity's dict() alternative.
    bytes16[] keyList; //  Declare array of keys. Our timestamps are of 16 bytes.

    function add(bytes16 _key, bytes memory _value) public {
        Input storage input = map_hashed[_key];
        input.value = _value;
        if (input.index > 0) {
            return; //  Return as input already exists.
        } else {
            keyList.push(_key); //  Add the key to keyList.
            uint256 keyListIndex = keyList.length - 1;
            input.index = keyListIndex + 1;
        }
    }

    function getByKey(bytes16 _key) public view returns (bytes memory) {
        return map_hashed[_key].value; //  Return hash of a given key.
    }

    function contains(bytes16 _key) public view returns (bool) {
        return map_hashed[_key].index > 0; //  Returns TRUE if key exists.
    }

    //  The functions below are not used in the program,
    //  but they may be used in >>truffle develop for testing.
    function size() public view returns (uint256) {
        return uint256(keyList.length);
    }

    function getByIndex(uint256 _index) public view returns (bytes memory) {
        require(_index >= 0, "Index must be greater than or equal to zero.");
        require(_index < keyList.length, "Specified index is too large.");
        return map_hashed[keyList[_index]].value;
    } //  Return hash if user specifies known index of a given key.

    function getKeys() public view returns (bytes16[] memory) {
        return keyList; // Get list of stored keys.
    }
}
