import sys, os
from json import load

# Configurations
main_directory = os.path.dirname(__file__)
absolute_path = os.path.join(main_directory, "../config/config.json")
with open(absolute_path) as config_file:
    config_data = load(config_file)
# Manipulation
welcome_message = config_data["welcome_message"]
date_format = config_data["date_format"]
uptime_format = config_data["uptime_format"]
memory_format = config_data["memory_format"]
pf_result = config_data["pf_result"]
should_display_blocks = config_data["should_display_blocks"]
should_display_text = config_data["should_display_text"]
should_display_keys = config_data["should_display_keys"]
color_block_node = config_data["color_block_node"]
divider_node = config_data["hr_divider_node"]
divider_repeat = config_data["hr_node_repeat"]
bullets = {
    "DEFAULT": config_data["default_bullet"],
    "INTERFACE": config_data["interface_bullet"],
    "MACHINE": config_data["machine_bullet"],
    "SHELL": config_data["shell_bullet"],
    "CPU": config_data["cpu_bullet"],
    "RAM": config_data["ram_bullet"],
    "UPTIME": config_data["uptime_bullet"],
    "DATE": config_data["date_bullet"]
}
word_wrap = config_data["word_wrap"]
# Colors
user_ = config_data["user_string_color"]
machine_ = config_data["machine_string_color"]
hr_ = config_data["hr_color"]
key_ = config_data["detail_key_color"]
val_ = config_data["detail_value_color"]
txt_ = config_data["text_description_color"]
bullet_ = {
    "DEFAULT": config_data["default_bullet_color"],
    "INTERFACE": config_data["interface_bullet_color"],
    "MACHINE": config_data["machine_bullet_color"],
    "SHELL": config_data["shell_bullet_color"],
    "CPU": config_data["cpu_bullet_color"],
    "RAM": config_data["ram_bullet_color"],
    "UPTIME": config_data["uptime_bullet_color"],
    "DATE": config_data["date_bullet_color"]
}
# Overrides
interface_override = config_data["interface_override"]
machine_override = config_data["machine_override"]
shell_override = config_data["shell_override"]
cpuram_override = config_data["cpuram_override"]
uptime_override = config_data["uptime_override"]
date_override = config_data["date_override"]
# FG Escape sequences
COLORS = {
    "black":            "\x1b[30m",
    "red":              "\x1b[31m",
    "green":            "\x1b[32m",
    "yellow":           "\x1b[33m",
    "blue":             "\x1b[34m",
    "magenta":          "\x1b[35m",
    "cyan":             "\x1b[36m",
    "white":            "\x1b[37m",
    "light black":      "\x1b[90m",
    "light red":        "\x1b[91m",
    "light green":      "\x1b[92m",
    "light yellow":     "\x1b[93m",
    "light blue":       "\x1b[94m",
    "light magenta":    "\x1b[95m",
    "light cyan":       "\x1b[96m",
    "light white":      "\x1b[97m"
}
END = "\x1b[0m"
BOLD = "\x1b[1m"
ITALIC = "\x1b[3m"
UNDERLINE = "\x1b[4m"


# Returns the user preferred color string
def color_(string_color):
    try:
        return COLORS[string_color]
    except KeyError:
        print("The color " + COLORS["red"] + "\"" + string_color + "\"" + END + \
              " is not a valid color. pls refer to gh page or doc for valid colors")
    sys.exit(0)


# Return machine make and model
def get_make_manufacture():
    from subprocess import run  # for manufacture
    if sys.platform == ("linux" or "linux2"):
        return "Linux"
    elif sys.platform == "darwin":
        sys_info = run([
            "system_profiler",
            "SPHardwareDataType"
            ], capture_output=True).stdout.decode()
        start_string = "Model Name: "
        start_index = sys_info.find(start_string) + len(start_string)
        return sys_info[start_index: sys_info.find("\n", start_index)]
    elif sys.platform == "win32":
        return "Windows"
    return sys.platform


# Returns os string "OS: macOS Big Sur v11.0.1"
def get_osstring():
    from subprocess import run  # for version
    osname = ""
    osversion = ""
    osversionname = ""
    if sys.platform == ("linux" or "linux2"):
        osname = "Linux"
    elif sys.platform == "darwin":
        osversion = run(["sw_vers", "-productVersion"], capture_output=True).stdout.decode().strip('\n')
        if osversion[0:5] == "10.14":
            osversionname = "Mojave"
        elif osversion[0:5] == "10.15":
            osversionname = "Catalina"
        elif osversion[0:4] == "11.0":
            osversionname = "Big Sur"
        osname = "macOS"
    elif sys.platform == "win32":
        osname = "Windows"
    else:
        osname = sys.platform
    return osname + " " + osversionname + " " + osversion


# Returns system uptime
def get_uptime():
    from subprocess import check_output  # for uptime
    uptime_string = check_output('uptime').decode().replace(',', '').split()
    if any(s in uptime_string for s in ['day','days']):
        days = int(uptime_string[2])
        if any(s in uptime_string for s in ['min', 'mins']):
            hrs = 0
            mins = uptime_string[4]
        else:
            hrs, mins = map(int, uptime_string[4].split(':'))
    elif any(s in uptime_string for s in ['min', 'mins']):
        days = 0
        hrs = 0
        mins = int(uptime_string[4])
    elif any(s in uptime_string for s in ['hr', 'hrs']):
        days = int(uptime_string[2])
        hrs = int(uptime_string[4])
        mins = 0
    else:
        days = 0
        hrs, mins = map(int, uptime_string[2].split(':'))
    if uptime_format == "hours":
        tot_hrs = (days * 24) + hrs
        return str(tot_hrs) + " hrs, " + str(mins) + " mins"
    elif uptime_format == "days":
        return str(days) + " days, " + str(hrs) + " hrs"
    elif uptime_format == "colon":
        return "{}:{}:{}".format(days, hrs, mins)
    return str(days) + " days, " + str(hrs) + " hrs, " + str(mins) + " mins"


# Returns current date string
def get_date():
    from datetime import datetime  # for date display
    if date_format == "full":
        return datetime.now().strftime("%b %d, %Y")
    elif date_format == "mmddyy":
        return datetime.now().strftime("%m / %d / %y")
    elif date_format == "daydd":
        return datetime.now().strftime("%A " + BOLD + "%d" + END)


# Returns shell string ZSH 5.8
def get_shellstring():
    from os import environ  # for machine info
    from subprocess import run  # shell version
    shell_type = environ['SHELL'].split('/')[-1].upper()
    current_version = ""
    if shell_type == "ZSH":
        shell_version = run(["zsh", "--version"], capture_output=True).stdout.decode()
        maybe_version = []
        for text in shell_version.split():
            try:
                maybe_version.append(float(text))
            except ValueError:
                pass
        if len(maybe_version) == 1:
            current_version = str(maybe_version[0])
    if shell_type == "BASH":
        shell_version = run(["bash", "--version"], capture_output=True).stdout.decode()
        start_string = "version "
        start_index = shell_version.find(start_string) + len(start_string)
        end_string = "(1)"
        current_version = shell_version[start_index: shell_version.find(end_string)]
    return shell_type + " " + current_version


# Returns user string "User \ machine"
def get_userstring():
    from os import environ, uname  # for machine info
    username = environ['USER'].upper()
    hostname = uname()[1]
    return color_(user_) + BOLD + username + END + \
        color_(machine_) + " \ " + hostname + END


# Returns system usage
def get_usage(choice):
    from psutil import virtual_memory  # for performance data
    cpu_use_string = ""
    ram_use_string = ""
    # Unit conversions
    divider = 2**30  # 1e+9
    if memory_format[1] == "MiB":
        divider = 2**20  # 1e+6
    # Actual values
    total = virtual_memory().total / divider
    available = virtual_memory().available / divider
    used = total - available
    # Actual percentages
    cpu_use_percent = available * 100 / total
    ram_use_percent = virtual_memory().percent
    if memory_format[0] == "percent":
        cpu_use_string = "{:.2f} %".format(cpu_use_percent)
        ram_use_string = "{:.2f} %".format(ram_use_percent)
    elif memory_format[0] == "values":
        cpu_use_string = "{:.2f} / {:.0f} {}".format(available, total, memory_format[1])
        ram_use_string = "{:.2f} / {:.0f} {}".format(used, total, memory_format[1])
    elif memory_format[0] == "both":
        cpu_use_string = "{:.2f} / {:.0f} {} ".format(available, total, memory_format[1]) + \
            BOLD + "({:.2f}%)".format(cpu_use_percent)
        ram_use_string = "{:.2f} / {:.0f} {} ".format(used, total, memory_format[1]) + \
            BOLD + "({:.2f}%)".format(ram_use_percent)
    return cpu_use_string if choice == "CPU" else ram_use_string


# Returns the color blocks for ANSI 1-16
def blocks_(type):
    x = 0
    y = 0
    if len(color_block_node.strip()) == 0:
        x = 4
        y = 10
    else:
        x = 3
        y = 9
    blocks = ""
    if type == "normal":
        for i in range(8):
            blocks += "\x1b[{}{}m".format(x, i) + color_block_node + END
    elif type == "bright":
        for i in range(8):
            blocks += "\x1b[{}{}m".format(y, i) + color_block_node + END
    if should_display_blocks == True:
        return blocks
    else:
        return ""


# Returns folded paragraph in array of sentences
def fold_paragraph(para):
    num_lines = len(para) / word_wrap # of lines
    if num_lines > round(num_lines) and num_lines % round(num_lines) > 0:
        num_lines += 1 - num_lines % round(num_lines)
    else:
        num_lines = round(num_lines)
    words = para.split(' ')
    columns_counted = 0
    temp_words = []
    sentences = []
    for word in words:
        if columns_counted <= word_wrap:
            columns_counted += len(word) + 1  # +1 space
            temp_words.append(word)
            if columns_counted >= word_wrap:
                columns_counted = 0
        if columns_counted == 0:
            sentence = ' '.join(temp_words)
            sentences.append(sentence)
            temp_words = []
    if len(sentences) < num_lines:
        para_sofar = ' '.join(sentences)
        remainder = para.replace(para_sofar, " ").strip()
        if len(remainder) > 0:
            sentences.append(remainder)
    for i, sentence in enumerate(sentences):
        sentences[i] = ITALIC + color_(txt_) + sentence + END
    return sentences


# Return detail string "NAME: detail information"
def detail(name, content):
    bullet = bullets["DEFAULT"]
    bullet_color = bullet_["DEFAULT"]
    if bullets[name] != "":
        bullet = bullets[name]
    if bullet_[name] != "":
        bullet_color = bullet_[name]
    spaces = " " * (12 - len(name))
    if should_display_keys == True:
        return (color_(bullet_color) + "{}" + color_(key_) + BOLD + "{}" + END + spaces + \
                color_(val_) + "{}" + END).format(bullet, name, content)
    else:
        return (color_(bullet_color) + "{}" + END + " " + color_(val_) + "{}" + END).format(bullet, content)



# Empty line
empty_line = ''
# ∙∙∙∙∙∙∙∙∙∙∙
divider_line = color_(hr_) + divider_node * divider_repeat + END


# Manipulate displayed data here
def detail_list():
    # Initialization details
    init_data = {}
    userstring = ""
    osstring = ""
    make_manufacture = ""
    shellstring = ""
    try:
        abs_path = os.path.join(main_directory, ".assist/details.json")
        with open(abs_path) as detail_file:
            init_data = load(detail_file)
        userstring = init_data["userstring"]
        osstring = init_data["osstring"] if interface_override == "" else interface_override
        make_manufacture = init_data["make_manufacture"] if machine_override == "" else machine_override
        shellstring = init_data["shellstring"] if shell_override == "" else shell_override
    except FileNotFoundError:
        print("Details not found... please initialize program with " + \
              COLORS["light green"] + "lewel init" + END)
        sys.exit(0)
    details = [
        blocks_("normal"),
        blocks_("bright"),
        empty_line,
        userstring,
        divider_line,
        detail("INTERFACE", osstring),
        detail("MACHINE",   make_manufacture),
        detail("SHELL",     shellstring),
        detail(pf_result,   get_usage(pf_result)),
        detail("UPTIME",    get_uptime()),
        detail("DATE",      get_date()),
        empty_line,
        ITALIC + color_(txt_) + welcome_message + END
    ]
    if cpuram_override is False:
        del details[-5]
    if uptime_override is False:
        del details[-4]
    if date_override is False:
        del details[-3]
    if should_display_text == False:
        del details[details.index(blocks_("bright"))+1:-1]
    if should_display_blocks == False:
        del details[0:details.index(userstring)]
    if len(welcome_message) > word_wrap:
        del details[-1]
        sentences = fold_paragraph(welcome_message)
        details.extend(sentences)
    return details
