from colorama import Fore
from dateutil import parser
import datetime


from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc

def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('Login to your [a]ccount')
    print('[L]ist your cages')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')
    # done: Get name & email
    name = input('name')
    email = input('email')

    # Done: Create account, set as logged in.

    old_acount = svc.find_account_by_email(email)
    if old_acount:
        error_msg("Error, that email already exists")
        return
    state.active_account = svc.create_account(name,email)
    success_msg(f"created an account with id {state.active_account.id}")


def log_into_account():
    print(' ****************** LOGIN **************** ')
    email = input('email please').strip().lower()

    account = svc.find_account_by_email(email)
    if not account:
        error_msg(f"doesn't exist with this mail {account}")
        return

    state.active_account = account
    success_msg('logged in successfully')
    # Done: Get email
    # Done: Find account in DB, set as logged in.

    # print(" -------- NOT IMPLEMENTED -------- ")


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')
    if not state.active_account:
        error_msg('You must login first')
        return

    try:
        meters = float(input('How many square meters is the cage?'))
    except:
        error_msg('Cancelled')

    carpeted = input("Is carpeted [y,n]?").lower().startswith('y')
    has_toys = input("Have snake toys [y,n]?").lower().startswith('y')
    allow_dangerous = input("can you keep poisonous snakes [y,n]?").lower().startswith('y')
    name = input("name for your cage would be?")
    price = float(input("how much you charging?"))
    cage = svc.register_cage(state.active_account,name,price,allow_dangerous,has_toys,carpeted,meters)
    state.reload_account() #to reflect the recently added data, we have to find it again
    success_msg(f'Registered new cage with id {cage.id}')
    # # TODO: Require an account
    # # TODO: Get info about cage
    # # TODO: Save cage to DB.
    #
    # print(" -------- NOT IMPLEMENTED -------- ")


def list_cages(suppress_header=False):
    if not suppress_header:
        print(' ******************     Your cages     **************** ')

    if not state.active_account:
        error_msg('You must login first to register a cage.')
        return

    cages = svc.find_cages_for_user(state.active_account)
    print(f"You have {len(cages)} cages.")
    for idx, c in enumerate(cages):
        print(f' {idx + 1}. {c.name} is {c.square_meters} meters.')
        for b in c.bookings:
            print('      * Booking: {}, {} days, booked? {}'.format(
                b.check_in_date,
                (b.check_out_date - b.check_in_date).days,
                'YES' if b.booked_date is not None else 'no'
            ))


def update_availability():
    #add avaialabilties for the cages you want to sell
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    list_cages(suppress_header=True)

    cage_number = input("Enter cage number: ")
    if not cage_number.strip():
        error_msg('Cancelled')
        print()
        return

    cage_number = int(cage_number)

    cages = svc.find_cages_for_user(state.active_account)
    selected_cage = cages[cage_number - 1]

    success_msg("Selected cage {}".format(selected_cage.name))

    start_date = parser.parse(
        input("Enter available date [yyyy-mm-dd]: ")
    )
    days = int(input("How many days is this block of time? "))

    svc.add_available_date(
        selected_cage,
        start_date,
        days
    )

    success_msg(f'Date added to cage {selected_cage.name}.')


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg("You must log in first to register a cage")
        return

    cages = svc.find_cages_for_user(state.active_account)

    bookings = [
        (c, b)
        for c in cages
        for b in c.bookings
        if b.booked_date is not None
    ]

    print("You have {} bookings.".format(len(bookings)))
    for c, b in bookings:
        print(' * Cage: {}, booked date: {}, from {} for {} days.'.format(
            c.name,
            datetime.date(b.booked_date.year, b.booked_date.month, b.booked_date.day),
            datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
            b.duration_in_days
        ))


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
