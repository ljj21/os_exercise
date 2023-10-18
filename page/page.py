# read the content of the physical memory
with open('physical_addr_content.txt', 'r') as file:
    physical_memory = []
    for line in file:
        for content in line[9:-1].split(' '):
            if content != '':
                physical_memory.append(int(content, 16))

page_size = 32  
virtual_address_space = 32 * 1024 
physical_memory_size = 4 * 1024
page_table_size = 32
page_directory_size = 32
pte_size = 1
pde_size = 1

page_bits = 5 # log2(page_size)
page_table_bits = 5 # log2(page_table_size)

pdbr = 0x220

def translate_virtual_to_physical(virtual_address):
    print(f"Virtual Address {hex(virtual_address)}:")

    pde_index = (virtual_address >> (page_bits + page_table_bits)) & (page_directory_size - 1)
    pte_index = (virtual_address >> page_bits) & (page_table_size - 1)
    offset = virtual_address & (page_size - 1)

    pde_address = pdbr + pde_index * pde_size
    pde_contents = physical_memory[pde_address]
    pde_valid = (pde_contents & 0x80) == 0x80
    print(f"  --> pde index: {hex(pde_index)} pde contents: (valid {int(pde_valid)} pfn {hex(pde_contents & 0x7f)})")

    if not pde_valid:
        print("    --> Fault (page directory entry not valid)")
        return
    
    pte_address = ((pde_contents & 0x7f)<< page_bits) + pte_index * pte_size
    pte_contents = physical_memory[pte_address]

    pte_valid = (pte_contents & 0x80) == 0x80
    print(f"    --> pte index: {hex(pte_index)} pte contents: (valid {int(pte_valid)} pfn {hex(pte_contents & 0x7f)})")

    if not pte_valid:
        print("      --> Fault (page table entry not valid)")
        return

    physical_address = ((pte_contents & 0x7f) << page_bits) + offset

    print(f"      --> Translates to Physical Address {hex(physical_address)} --> Value: {hex(physical_memory[physical_address])}")

virtual_addresses = [0x6c74, 0x6b22, 0x317a, 0x4546]

for virtual_address in virtual_addresses:
    translate_virtual_to_physical(virtual_address)