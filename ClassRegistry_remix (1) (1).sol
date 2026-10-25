// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ClassRegistry — Session 6 lab contract (Updated with Class & Student ID)
/// @notice Each address may register full student info exactly once.
///         The deployer (owner) can deregister a student (e.g. a typo entry).
contract ClassRegistry {
    // ---------------------------------------------------------- struct
    struct Student {
        string name;
        string className;
        string studentId;
    }

    // ---------------------------------------------------------- errors
    error AlreadyRegistered(address who);
    error NotRegistered(address who);
    error EmptyFields();
    error NotOwner();

    // ---------------------------------------------------------- events
    event Registered(address indexed who, string name, string className, string studentId);
    event Deregistered(address indexed who);

    // ---------------------------------------------------------- state
    address public immutable owner; // set once in the constructor, cheap to read

    mapping(address => Student) private _students; // who => Student info
    address[] private _members; // mappings can't be iterated → keep a list
    mapping(address => uint256) private _indexPlusOne; // who => index in _members + 1 (0 = absent)

    // ---------------------------------------------------------- modifiers
    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // ---------------------------------------------------------- writes
    /// @notice Đăng ký tài khoản với Tên, Lớp và MSSV (tạo 3 ô nhập ở nút register bên trái)
    function register(
        string calldata name, 
        string calldata className, 
        string calldata studentId
    ) external {
        if (bytes(name).length == 0 || bytes(className).length == 0 || bytes(studentId).length == 0) {
            revert EmptyFields();
        }
        if (_indexPlusOne[msg.sender] != 0) revert AlreadyRegistered(msg.sender);

        _students[msg.sender] = Student(name, className, studentId);
        _members.push(msg.sender);
        _indexPlusOne[msg.sender] = _members.length; // index + 1

        emit Registered(msg.sender, name, className, studentId);
    }

    /// @notice Owner removes a registration (swap-and-pop to keep the array dense).
    function deregister(address who) external onlyOwner {
        uint256 idxPlusOne = _indexPlusOne[who];
        if (idxPlusOne == 0) revert NotRegistered(who);

        uint256 idx = idxPlusOne - 1;
        uint256 lastIdx = _members.length - 1;
        if (idx != lastIdx) {
            address last = _members[lastIdx];
            _members[idx] = last;
            _indexPlusOne[last] = idx + 1;
        }
        _members.pop();
        delete _indexPlusOne[who];
        delete _students[who];

        emit Deregistered(who);
    }

    // ---------------------------------------------------------- reads
    function isRegistered(address who) public view returns (bool) {
        return _indexPlusOne[who] != 0;
    }

    /// @notice Tra cứu toàn bộ thông tin sinh viên theo địa chỉ ví
    function getStudent(address who) external view returns (
        string memory name, 
        string memory className, 
        string memory studentId
    ) {
        if (_indexPlusOne[who] == 0) revert NotRegistered(who);
        Student memory s = _students[who];
        return (s.name, s.className, s.studentId);
    }

    function memberCount() external view returns (uint256) {
        return _members.length;
    }

    function memberAt(uint256 index) external view returns (
        address who, 
        string memory name, 
        string memory className, 
        string memory studentId
    ) {
        who = _members[index];
        Student memory s = _students[who];
        return (who, s.name, s.className, s.studentId);
    }
}