#
# kimjt Network temporarily test tool
#
from api.sonatest import SonaTest
from ConfigParser import ConfigParser
from api.reporter2 import Reporter
import os
import commands

WHITE = '\033[1;97m'
BLUE = '\033[1;94m'
YELLOW = '\033[1;93m'
GREEN = '\033[1;92m'
RED = '\033[1;91m'
BLACK = '\033[1;90m'
BG_WHITE = '\033[0;97m'
BG_BLUEW = '\033[0;37;44m'
BG_SKYW = '\033[0;37;46m'
BG_PINKW = '\033[0;37;45m'
BG_YELLOWW = '\033[0;30;43m'
BG_GREENW = '\033[0;37;42m'
BG_RED = '\033[0;91m'
BG_BLACK = '\033[0;90m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

CONFIG_FILE = '../config/config.ini'

test = SonaTest(CONFIG_FILE)

MAIN_MENU = 1
SCEN_MENU = 2
ETC_MENU = 3

navi_menu = MAIN_MENU
exit_flag=True


SCENARIO_PATH = './'

def title_print(menu='None'):
    Reporter.PRINTB("|--------------------------|")
    print BLUE + '|' + BG_BLUEW + \
                     '       SONA-TOOL          ' + BLUE + '|'+ENDC
    Reporter.PRINTB("|--------------------------|")
    if 'None' not in menu:
        print BLUE + '|' + BG_PINKW + \
                      menu.ljust(26) + BLUE + '|'+ENDC
        Reporter.PRINTB("|--------------------------|")

def main_menu():
    os.system('clear')
    title_print()
    Reporter.PRINTB("| 1. create scenario start |")
    Reporter.PRINTB("| 2. delete scenario start |")
    Reporter.PRINTB("| 3. create scenario       |")
    Reporter.PRINTB("| 4. delete scenario       |")
    Reporter.PRINTB("| 5. etc test              |")
    Reporter.PRINTB("| 6. exit                  |")
    Reporter.PRINTB("|--------------------------|")

def state_test_menu():
    os.system('clear')
    title_print(' # etc test')
    Reporter.PRINTB("| 1. onos state            |")
    Reporter.PRINTB("| 2. traffic test          |")
    Reporter.PRINTB("| 3. return to main menu   |")
    Reporter.PRINTB("|--------------------------|")

def scen_delete_menu():
    os.system('clear')
    title_print(' # create scenario')
    Reporter.PRINTB("| 1. delete_netowk         |")
    Reporter.PRINTB("| 2. delete_subnet         |")
    Reporter.PRINTB("| 3. delete_router         |")
    Reporter.PRINTB("| 4. remove_router_interface|")
    Reporter.PRINTB("| 5. security_group        |")
    Reporter.PRINTB("| 6. create_instance       |")
    Reporter.PRINTB("| 7. floatingip_associate  |")
    Reporter.PRINTB("| 8. return to main menu   |")
    Reporter.PRINTB("|--------------------------|")

def scen_create_menu():
    os.system('clear')
    title_print(' # create scenario')
    Reporter.PRINTB("| 1. create_netowk         |")
    Reporter.PRINTB("| 2. create_subnet         |")
    Reporter.PRINTB("| 3. create_router         |")
    Reporter.PRINTB("| 4. add_router_interface  |")
    Reporter.PRINTB("| 5. security_group        |")
    Reporter.PRINTB("| 6. create_instance       |")
    Reporter.PRINTB("| 7. floatingip_associate  |")
    Reporter.PRINTB("| 8. return to main menu   |")
    Reporter.PRINTB("|--------------------------|")


def report_log_viewer():
    while 1:
        sel_log = raw_input("\n Do you want to view the log? (y/n) ")
        if 'y' in sel_log:
            print 'report file : ', Reporter.report_file_name
            (exitstatus, outtext) = commands.getstatusoutput('cat '+ Reporter.report_file_name)
            print outtext
            print '\n================================== END LOG ==================================\n\n'
            ret = raw_input(RED + "\n press any key to ENTER " + ENDC)
            if ret:
                break
        elif 'n' in sel_log:
            break
        else:
            Reporter.PRINTR('invalid value, retry! ')
            continue




def scenario_file_search(type):
    file_list=[]
    filenames = os.listdir(SCENARIO_PATH)
    for filename in filenames:
        full_filename = os.path.join(SCENARIO_PATH, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.ini':
            if type + '_scenario' in full_filename:
                file_name = full_filename.split('/')[-1]
                file_list.append((file_name.split('.ini'))[0])

    return file_list

def get_config_key_list(section):
    config = ConfigParser()
    config.read(CONFIG_FILE)
    item = config._sections[section]
    key_list = item.keys()
    del key_list[0]
    return key_list

def create_scenario_start():
    os.system('clear')
    #### scen file ####
    scen_list = scenario_file_search('create')
    title_print(' # create scenario start')
    for i in range(len(scen_list)):
        Reporter.PRINTB('| %d. %-22s|', i+1, scen_list[i])
    Reporter.PRINTB('| %d. return to main menu   |', len(scen_list)+1)
    Reporter.PRINTB("|--------------------------|")
    sel_scen = input('select scenario :')
    if 4 is sel_scen:
        return
    create_start_scenario(scen_list[sel_scen-1])

def delete_scenario_start():
    os.system('clear')
    #### scen file ####
    scen_list = scenario_file_search('delete')
    title_print(' # delete scenario start')
    for i in range(len(scen_list)):
        Reporter.PRINTB('| %d. %-22s|', i+1, scen_list[i])
    Reporter.PRINTB('| %d. return to main menu   |', len(scen_list)+1)
    Reporter.PRINTB("|--------------------------|")
    sel_scen = input('select scenario :')
    if 4 is sel_scen:
        return
    ##### start secnario ####
    delete_start_scenario(scen_list[sel_scen-1])

def display_scenario(scen_name):
    os.system('clear')
    scen_file = SCENARIO_PATH+scen_name+'.ini'
    scen_ini = ConfigParser()
    scen_ini.read(scen_file)

    net_item = (scen_ini._sections['network']).values(); del net_item[0]
    sub_item = (scen_ini._sections['subnet']).values(); del sub_item[0]
    router_item = (scen_ini._sections['router']).values(); del router_item[0]
    router_if_item = (scen_ini._sections['router-interface']).values(); del router_if_item[0]
    sg_item = (scen_ini._sections['security_group']).values(); del sg_item[0]
    inst_item = (scen_ini._sections['instance']).values(); del inst_item[0]
    size_list=[]
    size_list.append(len(' | '.join(net_item)))
    size_list.append(len(' | '.join(sub_item)))
    size_list.append(len(' | '.join(router_item)))
    size_list.append(len(' | '.join(router_if_item)))
    size_list.append(len(' | '.join(sg_item)))
    size_list.append(len(' | '.join(inst_item)))
    max_size = max(size_list)

    if 'create' in scen_name:
        fip_as_item = (scen_ini._sections['floatingip_associate']).values(); del fip_as_item[0]

    title_size = (max_size/2)-2

    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))
    print YELLOW + '|' + BOLD + BG_YELLOWW + ' scenario information : ' + scen_name + \
          ' '.ljust(max_size-len(scen_name)+1) + YELLOW + '|' + ENDC
    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))
    print YELLOW + '|' + BOLD + BG_YELLOWW + '          Type         ' + \
          YELLOW + '|' + BOLD + BG_YELLOWW + ' '.ljust(title_size+1) + \
          'Value'.ljust(max_size-title_size) + YELLOW + '|' + ENDC

    Reporter.PRINTY('|=======================|%s|', ('='*(max_size+1)).ljust(max_size+1))
    Reporter.PRINTY('| Network               | %s|', ' | '.join(net_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Subnet                | %s|', ' | '.join(sub_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Router                | %s|', ' | '.join(router_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Router_Interface      | %s|', ' | '.join(router_if_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Security_Group        | %s|', ' | '.join(sg_item).ljust(max_size))
    Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
    Reporter.PRINTY('| Instance              | %s|', ' | '.join(inst_item).ljust(max_size))
    if 'create' in scen_name:
        Reporter.PRINTY('|-----------------------|%s|', ('-'*max_size).ljust(max_size+1))
        Reporter.PRINTY('| Floating_ip_associate | %s|', ' | '.join(fip_as_item).ljust(max_size))
    Reporter.PRINTY('|------------------------%s|', ('-'*(max_size+1)).ljust(max_size+1))

    while 1:
        sel_scen = raw_input(" Do you want to start the scenario? (y/n) ")
        if 'y' in sel_scen:
            return True
        elif 'n' in sel_scen:
            return False
        else:
            print 'invalid value, retry ... '
            continue

def create_start_scenario(scen_name):
    ret = display_scenario(scen_name)
    if False is ret:
        return False

    global test
    scen_file = SCENARIO_PATH+scen_name+'.ini'
    scen_ini = ConfigParser()
    scen_ini.read(scen_file)

    # Network
    item = scen_ini._sections['network']
    for i in range(len(item)):
        if i is not 0:
            test.network.create_network(item.values()[i])

    # SubNet
    item = scen_ini._sections['subnet']
    for i in range(len(item)):
        if i is not 0:
            test.network.create_subnet((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])

    # Router
    item = scen_ini._sections['router']
    for i in range(len(item)):
        if i is not 0:
            test.network.create_router((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])

    item = scen_ini._sections['router-interface']
    for i in range(len(item)):
        if i is not 0:
            test.network.add_router_interface((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])

    # Security Group
    item = scen_ini._sections['security_group']
    arg2 = []
    for i in range(len(item)):
        if i is not 0:
            for x in range(len((item.values()[i]).split(', '))):
                if x is 0:
                    arg1 = (item.values()[i]).split(', ')[x]
                else:
                    arg2.append((item.values()[i]).split(', ')[x])

            test.network.create_securitygroup(arg1, ', '.join(arg2))

    # Instance
    item = scen_ini._sections['instance']
    for i in range(len(item)):
        if i is not 0:
            if 2 is len((item.values()[i]).split(', ')):
                test.instance.create_instance((item.values()[i]).split(', ')[0],
                                             (item.values()[i]).split(', ')[1], '')
            elif 3 is len((item.values()[i]).split(', ')):
                test.instance.create_instance((item.values()[i]).split(', ')[0],
                                             (item.values()[i]).split(', ')[1],
                                             (item.values()[i]).split(', ')[2])
            else:
                print 'invalid argument'

    # # Floating IP
    item = scen_ini._sections['floatingip_associate']
    for i in range(len(item)):
        if i is not 0:
            test.instance.floatingip_associate((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])
            test.floating_ip_check((item.values()[i]).split(', ')[0])

    test.reporter.test_summary()
    Reporter.initial_test_count()

    ## View Log???? ##
    report_log_viewer()

def delete_start_scenario(scen_name):
    ret = display_scenario(scen_name)
    if False is ret:
        return False

    # global test
    scen_file = SCENARIO_PATH+scen_name+'.ini'
    scen_ini = ConfigParser()
    scen_ini.read(scen_file)

    # Instance
    item = scen_ini._sections['instance']
    for i in range(len(item)):
        if i is not 0:
            test.instance.delete_instance((item.values()[i]).split(', ')[0])

    # Floating IP
    test.instance.delete_floatingip_all()

    # Security Group
    item = scen_ini._sections['security_group']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_seuritygroup((item.values()[i]).split(', ')[0])

    # Router interface
    item = scen_ini._sections['router-interface']
    for i in range(len(item)):
        if i is not 0:
            test.network.remove_router_interface((item.values()[i]).split(', ')[0],
                                       (item.values()[i]).split(', ')[1])
    # Router
    item = scen_ini._sections['router']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_router((item.values()[i]).split(', ')[0])

    # SubNet
    item = scen_ini._sections['subnet']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_subnet((item.values()[i]).split(', ')[0])
    # Network
    item = scen_ini._sections['network']
    for i in range(len(item)):
        if i is not 0:
            test.network.delete_network(item.values()[i])

    test.reporter.test_summary()
    Reporter.initial_test_count()
    report_log_viewer()


# scenario config
# main menu function
def scen_delete_menu():
    print 'delete_scenario'

def scenario_test_start():
    print 'scenario_test_start'

# scenaro create function
def create_network():
    print 'create network'
    # network name list print
    sel = input(BLACK+'sel : '+ENDC)



def create_subnet(subnet, network):
    print subnet, network

def create_router(router):
    print router

def add_router_interface(router, subnet):
    print router, subnet

def create_security_group():
    print 'create_security_group'

def create_instance():
    print 'create_instance'

def floatingip_associate():
    print 'floatingip_associate'

def onos_state():
    print 'onos_state'

def traffic_test():
    print 'traffic_test'

def termination():
    print 'termination!!!!!'
    global exit_flag
    exit_flag=False


main_menu_map = {
    1:create_scenario_start,
    2:delete_scenario_start,
    3:scen_create_menu,
    4:scen_delete_menu,
    5:state_test_menu,
    6:termination
}

scen_menu_map = {
    1:create_network,
    2:create_subnet,
    3:create_router,
    4:add_router_interface,
    5:create_security_group,
    6:create_instance,
    7:floatingip_associate,
    8:main_menu
}

etc_menu_map = {
    1:onos_state,
    2:traffic_test,
    3:main_menu
}


PROMPT = BOLD + WHITE + ' Select Menu : '+ENDC

def main():
    global exit_flag
    main_menu()
    while exit_flag:
        try:
            global navi_menu
            if MAIN_MENU is navi_menu:
                menu = input(PROMPT)
                main_menu_map.get(menu)()
                if 3 is menu:
                    navi_menu = SCEN_MENU
                elif 5 is menu:
                    navi_menu = ETC_MENU
                elif 6 is menu:
                    break
                else:
                    main_menu()
            elif SCEN_MENU is navi_menu:
                menu = input(PROMPT)
                scen_menu_map.get(menu)()
                if 8 is menu:
                    navi_menu = MAIN_MENU
                else:
                    scen_create_menu()
            elif ETC_MENU is navi_menu:
                menu = input(PROMPT)
                etc_menu_map.get(menu)()
                if 3 is menu:
                    navi_menu = MAIN_MENU
                else:
                    state_test_menu()
        except Exception, e:
            # print 'Invailid command!'
            print 'err : ', e
            if MAIN_MENU is navi_menu:
                main_menu()
            elif SCEN_MENU is navi_menu:
                scen_create_menu()
            elif ETC_MENU is navi_menu:
                state_test_menu()
            # print e
            continue

main()
