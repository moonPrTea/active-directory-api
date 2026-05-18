from enum import Enum

class GroupStatus(str, Enum):
    NOT_FOUND_GROUP = "Group with current title doesn't exist"
    GROUP_ALREADY_EXISTS = "Group already exists"
    NO_MEMBERS_IN_GROUP = "No members were found in current employee group"

