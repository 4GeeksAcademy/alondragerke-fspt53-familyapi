
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [
            {
                "id": self._generateId(),
                "first_name": "John",
                "last_name": self.last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generateId(),
                "first_name": "Jane",
                "last_name": self.last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 31]
            },
            {
                "id": self._generateId(),
                "first_name": "Jimmy",
                "last_name": self.last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member_id = member.get("id") or self._generateId()
        member["id"] = member_id
        self._members.append(member)

    def delete_member(self, id):
        for index, member in enumerate(self._members):
            if member["id"] == id:
                del self._members[index]
                return True
        return False

    def update_member(self, id, member):
        for index, existing_member in enumerate(self._members):
            if existing_member["id"] == id:
                member["id"] = id
                self._members[index] = member
                return True, "Member updated successfully"
        return False, "Member not found"


    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
