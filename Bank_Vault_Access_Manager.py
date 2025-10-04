import os

# Message strings for copy and paste:
# "Unauthorized access. Employee ID {employee_id} not authorized to access the vault.")
# "Unauthorized access. Employee ID {employee_id} not recognized."
# "Access not granted."
# "Authorized Access for {self.employee_id}. Performed activity inside the bank vault: {activity}"
# "Activity not allowed. Access not granted."
#

class VaultAccessControl:
    
    def __init__(self, authorized_employees, all_employees):
        self.authorized_employees = set(authorized_employees)
        self.all_employees = set(all_employees)
        self.access_granted = False
        self.employee_id = None

    def grant_access(self, employee_id):
        self.employee_id = employee_id
        
        if employee_id not in self.all_employees:
            raise ValueError(f"Unauthorized access. Employee ID {employee_id} not recognized.")
            
        if employee_id not in self.authorized_employees:
            raise PermissionError(f"Unauthorized access. Employee ID {employee_id} not authorized to access the vault.")
        self.access_granted = True

    def release_access(self):
        self.access_granted = False
        self.employee_id = None

class BankVaultAccessManager:
    def __init__(self, employee_id, access_control):
        self.employee_id = employee_id
        self.access_control = access_control
        self.error = None

    def __enter__(self):
        try:
            self.access_control.grant_access(self.employee_id)
            
        except (ValueError, PermissionError) as e:
            self.error = str(e)
            
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.access_control.release_access()

    def perform_activity(self, activity):
        if self.error:
            return f"Error occurred: {self.error}"
            
        if self.access_control.access_granted:
            return f"Authorized Access for {self.employee_id}. Performed activity inside the bank vault: {activity}"
            
        return "Activity not allowed. Access not granted."

# Driver Code
if __name__ == "__main__":
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input())
    all_employees_input = input()
    all_employees = [emp.strip() for emp in all_employees_input.split(",")]
    m = int(input())
    authorized_employees_input = input()
    authorized_employees = [emp.strip() for emp in authorized_employees_input.split(",")]
    access_control = VaultAccessControl(authorized_employees, all_employees)
    q = int(input())
    users_input = input()
    users = [user.strip() for user in users_input.split(",")]    
    for user in users:
        try:
            with BankVaultAccessManager(user, access_control) as vault:
                result = vault.perform_activity("Counting cash")
                fptr.write(result)
                fptr.write('\n')
        except ValueError as e:
            fptr.write(f"Error occurred: {str(e)}")
            fptr.write('\n')
    fptr.close()
