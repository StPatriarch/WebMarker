from moduls import options


def loop():
    opt = options.user_options
    options.clear_screen()
    options.print_options(opt)
    chosen_options = options.getting_user_choice(opt)
    options.clear_screen()
    chosen_options.choose()
    _ = input('Enter for return main menu')


if __name__ == '__main__':
    while True:
        loop()
