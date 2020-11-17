#!/usr/bin/python3

import re

t = "t"
action_proc = "action_proc"
action_bus = "action_bus"
data_src = "data_src"
state_p = "state_p"

initial = "initial"
na = "-"

Rd = "Rd"
Wr = "Wr"

M_state = "M"
E_state = "E"
S_state = "S"
I_state = "I"

BusRd_mag_action = "BusRd"
BusRdX_mag_action = "BusRdX"
Flush_mag_action = "Flush"

Cache_src = "Cache"
Mem_src = "Mem"
Flush_src = "Flush"


class MESI:
    def __init__(self, nr_of_proc, proc_actions):
        self.nr_of_proc = nr_of_proc
        self.proc_actions = proc_actions
        self.table = []

        self.table_row = {
            t: None,
            action_proc: None,
            action_bus: None,
            data_src: None
        }
        for i in range(self.nr_of_proc):
            self.table_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] = None

    def do_actions(self):
        for row_index in range(len(self.proc_actions) + 1):
            row = self.table_row.copy()
            self.table.append(row)

            row[t] = row_index

            if row_index == 0:
                row[action_proc] = initial
                row[action_bus] = na
                row[data_src] = na
                for i in range(self.nr_of_proc):
                    row["{state_p}{i}".format(state_p=state_p, i=i + 1)] = I_state

            else:
                action_index = row_index - 1
                row[action_proc] = self.proc_actions[action_index]

                if Rd in self.proc_actions[action_index]:
                    self.do_read(action=self.proc_actions[action_index],
                                 previous_row=self.table[row_index - 1],
                                 crt_row=self.table[row_index])
                elif Wr in self.proc_actions[action_index]:
                    self.do_write(action=self.proc_actions[action_index],
                                  previous_row=self.table[row_index - 1],
                                  crt_row=self.table[row_index])
                else:
                    print("[ERROR] Invalid action: '{action}'".format(action=self.proc_actions[action_index]))

    def do_read(self, action, previous_row, crt_row):
        proc_nrs = re.findall('P(.*?)Rd', action)
        if proc_nrs == []:
            print("[ERROR] Invalid processor specification in read action '{action}'".format(action=action))
            return
        proc_nr = int(proc_nrs[0])

        # check if all states are Invalid
        all_invalid = True
        for i in range(self.nr_of_proc):
            if previous_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] != I_state:
                all_invalid = False
                break
        if all_invalid is True:
            crt_row["{state_p}{i}".format(state_p=state_p, i=proc_nr)] = E_state
            crt_row[data_src] = Mem_src
            crt_row[action_bus] = BusRd_mag_action
            # update all the other states too
            self.update_states(previous_row=previous_row, crt_row=crt_row, exclusions=[proc_nr])
            return

        # check if any OTHER state is Shared
        if previous_row["{state_p}{i}".format(state_p=state_p, i=proc_nr)] != S_state:
            shared_state_exists = False
            shared_state_proc = None
            for i in range(self.nr_of_proc):
                if previous_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] == S_state:
                    shared_state_exists = True
                    shared_state_proc = i + 1
                    break
            if shared_state_exists is True:
                crt_row["{state_p}{i}".format(state_p=state_p, i=proc_nr)] = S_state
                crt_row[data_src] = "{Cache}{proc_nr}".format(Cache=Cache_src, proc_nr=shared_state_proc)
                crt_row[action_bus] = Flush_mag_action
                # update all the other states too
                self.update_states(previous_row=previous_row, crt_row=crt_row, exclusions=[proc_nr])
                return

        # check if any OTHER state is Exclusive or Modified
        exclusive_state_exists = False
        exclusive_state_proc = None
        prev_state = None
        for i in range(self.nr_of_proc):
            if i + 1 != proc_nr:
                if previous_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] in [E_state, M_state]:
                    crt_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] = S_state
                    exclusive_state_exists = True
                    exclusive_state_proc = i + 1
                    prev_state = previous_row["{state_p}{i}".format(state_p=state_p, i=i + 1)]
                    break
        if exclusive_state_exists is True:
            crt_row["{state_p}{i}".format(state_p=state_p, i=proc_nr)] = S_state
            crt_row[data_src] = "{Cache}{proc_nr}".format(Cache=Cache_src, proc_nr=exclusive_state_proc)
            if prev_state == E_state:
                crt_row[action_bus] = Flush_mag_action
            else:
                crt_row[action_bus] = BusRd_mag_action
            # update all the other states too
            self.update_states(previous_row=previous_row, crt_row=crt_row, exclusions=[proc_nr, exclusive_state_proc])
            return

        # keep the same state
        self.update_states(previous_row=previous_row, crt_row=crt_row, exclusions=[])
        crt_row[data_src] = na
        crt_row[action_bus] = na

    def do_write(self, action, previous_row, crt_row):
        proc_nrs = re.findall('P(.*?)Wr', action)
        if proc_nrs == []:
            print("[ERROR] Invalid processor specification in write action '{action}'".format(action=action))
            return
        proc_nr = int(proc_nrs[0])

        crt_row["{state_p}{i}".format(state_p=state_p, i=proc_nr)] = M_state
        for i in range(self.nr_of_proc):
            if i + 1 != proc_nr:
                crt_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] = I_state

        crt_row[action_bus] = BusRdX_mag_action
        crt_row[data_src] = Flush_mag_action

    def update_states(self, previous_row, crt_row, exclusions):
        for i in range(self.nr_of_proc):
            if i + 1 not in exclusions:
                crt_row["{state_p}{i}".format(state_p=state_p, i=i + 1)] = \
                    previous_row["{state_p}{i}".format(state_p=state_p, i=i + 1)]

    def print_table(self):
        header_to_print = ["t", "ActionProc"]
        for i in range(self.nr_of_proc):
            header_to_print.append("P{nr}".format(nr=i + 1))
        header_to_print.append("ActionBus")
        header_to_print.append("DataSrc")

        to_print = [header_to_print]

        for row in self.table:
            row_to_print = [str(row[t]), row[action_proc]]
            for i in range(self.nr_of_proc):
                row_to_print.append(row["{state_p}{i}".format(state_p=state_p, i=i + 1)])
            row_to_print.append(row[action_bus])
            row_to_print.append(row[data_src])

            to_print.append(row_to_print)

        col_width = max(len(word) for row in to_print for word in row)
        print('-' * (col_width + 1) * len(header_to_print))
        for row in to_print:
            padded_row = [word.center(col_width) for word in row]
            blocks_to_string = "|"
            for block in padded_row:
                blocks_to_string += str(block) + "|"
            print(blocks_to_string)
            print('-' * len(blocks_to_string))


def main():
    nr_of_proc = 4
    proc_actions = ["P1Rd", "P2Rd", "P3Rd", "P4Rd", "P1Rd", "P1Wr", "P1Rd", "P2Wr", "P3Rd", "P4Wr", "P4Rd", "P1Rd"]

    mesi = MESI(nr_of_proc=nr_of_proc, proc_actions=proc_actions)
    mesi.do_actions()
    mesi.print_table()


if __name__ == '__main__':
    main()
