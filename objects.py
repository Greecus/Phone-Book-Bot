from collections import UserDict

class ContactExistanceError(ValueError):
    pass

class NumberExistanceError(ValueError):
    pass

class MissingArgumentError(TypeError):
    pass

class Name:
    def __init__(self,name:str):
        self.value=name

class Phone:
    def __init__(self,phone_number:str):
        self.number=phone_number

class Record:
    def __init__(self,name:Name,*phone_nums:Phone):
        self.name=name
        self.phones=[]
        if len(phone_nums): 
            for phone in phone_nums:
                self.phones.append(phone)
        
    def add(self,phone_number):
        for phone in self.phones:
            if phone.number==phone_number:
                raise NumberExistanceError('This contact already had this number')
        self.phones.append(Phone(phone_number))
    
    def remove(self,phone_number):
        for phone in self.phones:
            if phone_number==phone.number:
                self.phones.remove(phone)
                return 
        raise NumberExistanceError("This contact doesn't have this number")
        
    def change(self,previous_number,new_number):
        try:
            index=[phone.number for phone in self.phones].index(previous_number)
        except ValueError:
            raise NumberExistanceError("Phone number you are trying to change doesn't exist")
        for phone in self.phones:
            if phone.number==new_number:
                raise NumberExistanceError('Phone number to which you are trying to change is already on this contacts list')
        self.phones[index]=Phone(new_number)
        
class AddressBook(UserDict):
    def __init__(self,*records:Record):
        self.records:dict[str,Record]={}
        if len(records):
            for record in records:
                self.records.update({record.name.value:record})

    def add_contact(self,name:str)->None:
        #if self.records.get(name): raise ContactExistanceError('Contact with that name already exists')
        if not self.records.get(name): 
            record=Record(name)
            self.records.update({record.name:record})

    def _does_contact_exist(func):
        def inner(self,name,*args):
            if not self.records.get(name): raise ContactExistanceError("Contact with this name doesn't exist")
            return func(self,name,*args)

        return inner
    
    @_does_contact_exist
    def add_phone_num(self,name:str,phone_number:str=None)->None:
        self.records[name].add(phone_number)

    @_does_contact_exist
    def change_phone_num(self,name:str,previous_phone_num:str,new_phone_num:str)->None:
        self.records[name].change(previous_phone_num,new_phone_num)

    @_does_contact_exist
    def see_contacts_phone_numbers(self,name:str)->list:
        return [phone.number for phone in self.records[name].phones]
    
    @_does_contact_exist
    def remove_contact(self,name:str)->None:
        self.records.pop(name)
    
    @_does_contact_exist
    def remove_number(self,name:str,number:str)->None:
        self.records[name].remove(number)

class Field:
    pass    



