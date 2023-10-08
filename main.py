from objects import AddressBook,ContactExistanceError,NumberExistanceError,MissingArgumentError
adress_book=AddressBook()

def main()->None:
    global running
    command= input('\nPlease give me command ').casefold()
    if command=='.':
        running=False
    elif command in ["good bye","close","exit","bye"]:
        running=False
        print("Good bye!")
    elif command=='hello':
        print("How can I help you?")
    elif command=='show all':
        print(''.join(f"{name}\n" for name in adress_book.records.keys()))
    elif command in ['help','?']:
        print(f"{'List of Commands':^48}\n"\
            f"{'help':>22} - list of commands\n"\
            f"{'exit':>22} - closing app\n"\
            f"{'hello':>22} - exchanging pleasantries\n"\
            f"{'show all':>22} - show all contacts names\n"\
            f"{'phone [name]':>22} - check phone number under given name\n"\
            f"{'add [name] [phone]':>22} - adding new phone number\n"\
            f"{'change [name] [phone]':>22} - changing phone number of existing contact\n"
            f"{'remove [name] [phone]':>22} - if only name given remove contact if name and number remove phone number from contact\n")
    else:
        command=command.split()
        if command[0]=='change':
            print(change_contact(*command[1:]))
        elif command[0]=='add':
            print(add_contact(*command[1:]))
        elif command[0] == 'phone':
            print(phone(*command[1:]))
        elif command[0] == 'remove':
            print(remove(*command[1:]))
        else:
            print("Command not recognized. Type \'help\' for command list")
    
def input_error(func):
    def inner(*args):
        try:
            output=func(*args)
        except ContactExistanceError as e:
            return e
        except NumberExistanceError as e:
            return e
        except MissingArgumentError as e:
            return e
        return output
    return inner

@input_error
def add_contact(name:str=None, phone:str=None)->str:
    if not name or not phone:   raise MissingArgumentError('Missing phone number or name')
    adress_book.add_contact(name)
    adress_book.add_phone_num(name, phone)
    return 'Contact added'

@input_error
def change_contact(name:str=None,previous_phone_num:str=None,new_phone_num:str=None):
    if not name or not previous_phone_num or not new_phone_num:   raise MissingArgumentError('Missing arguments')
    adress_book.change_phone_num(name,previous_phone_num,new_phone_num)
    return "Phone number changed"

@input_error
def phone(name:str=None)->str:
    if not name: raise MissingArgumentError('Missing name')
    phone_number=adress_book.see_contacts_phone_numbers(name)
    return '\n'.join(f'{phone}' for phone in [f'  {name}']+phone_number)

@input_error
def remove(name:str=None, phone_number:str=None):
    if not name: raise MissingArgumentError('Missing arguments')
    if phone_number:
        adress_book.remove_number(name,phone_number)
        return "Phone number removed"
    else:
        adress_book.remove_contact(name)
        return 'Contact removed'
    
running=True
while running:
    main()