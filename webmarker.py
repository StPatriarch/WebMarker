from moduls import options


if __name__ == '__main__':
    opt = options.user_options
    options.print_options(opt)
    chosen_options = options.getting_user_choice(opt)
    chosen_options.choose()
