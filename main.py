from objects import AddressBook,ContactExistanceError,NumberExistanceError,MissingArgumentError,WrongInputError
from colorama import just_fix_windows_console, Fore
adress_book=AddressBook()
just_fix_windows_console()
def main()->None:
    global running
    command= input(Fore.BLUE+'\nPlease give me command ').casefold()
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
            f"{'show [number]':>22} - show contacts names with specified number of contacts per page\n"\
            f"{'phone [name]':>22} - check phone number under given name\n"\
            f"{'add [name] [phone]':>22} - adding new phone number\n"\
            f"{'change [name] [phone]':>22} - changing phone number of existing contact\n"
            f"{'remove [name] [phone]':>22} - if only name given remove contact if name and number remove phone number from contact\n")
    else:
        command=command.split()
        if command[0]=='show':
            show_contacts(*command[1:])
        elif command[0]=='change':
            change_contact(*command[1:])
        elif command[0]=='add':
            add_contact_and_phone(*command[1:])
        elif command[0] == 'phone':
            phone(*command[1:])
        elif command[0] == 'remove':
            remove(*command[1:])
        else:
            print("Command not recognized. Type \'help\' for command list")
    
def input_error(func):
    def inner(*args):
        try:
            func(*args)
        except ContactExistanceError as e:
            print(e)
        except NumberExistanceError as e:
            print(e)
        except MissingArgumentError as e:
            print(e)
        except WrongInputError as e:
            print(e)
    return inner

@input_error
def show_contacts(contacts_per_page=9999,*args):
    try:
        contacts_per_page=int(contacts_per_page)
    except ValueError:
        raise WrongInputError("Input for 'show' command has to be 'all' or number of records per page") 
    iterator=adress_book.iterator(contacts_per_page)
    for i,page in enumerate(iterator):
        print(f'\nPage {i+1}')
        print(''.join(f"{name}\n" for name in page))
        print(" n - next page\n e - exit from address book")
        command=input()
        while command not in ['n','e']:
            command=input("give valid command: ")
        if command=='e':
            break


@input_error
def add_contact_and_phone(name:str=None, phone:str=None)->None:
    if not name:   raise MissingArgumentError('Missing name')
    adress_book.add_contact(name)
    adress_book.add_phone_num(name, phone)
    print('Contact added')

@input_error
def change_contact(name:str=None,previous_phone_num:str=None,new_phone_num:str=None)->None:
    if not name or not previous_phone_num or not new_phone_num:   raise MissingArgumentError('Missing arguments')
    adress_book.change_phone_num(name,previous_phone_num,new_phone_num)
    print("Phone number changed")

@input_error
def phone(name:str=None)->None:
    if not name: raise MissingArgumentError('Missing name')
    phone_number=adress_book.see_contacts_phone_numbers(name)
    print('\n'.join(f'{phone}' for phone in [f'  {name}']+phone_number))

@input_error
def remove(name:str=None, phone_number:str=None)->None:
    if not name: raise MissingArgumentError('Missing arguments')
    if phone_number:
        adress_book.remove_number(name,phone_number)
        print("Phone number removed")
    else:
        adress_book.remove_contact(name)
        print('Contact removed')
    
running=True
while running:
    main()