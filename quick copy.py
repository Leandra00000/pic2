import os
import subprocess
import matplotlib.pyplot as plt

def create_trace_sequential_columns(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}_c.trace"

    max_columns = (1 << 10)  # 10 bits for columns, i.e., 1024
    row_bits = 16
    bank_bits = 2
    bank_group_bits = 1
    offset_bits = 3

    # Counters for the fields in the address
    row = 0
    bank_group = 0
    bank = 0
    column = 0

    with open(filename, 'w') as f:
        for i in range(num_writes):
            if column >= max_columns:  # Column overflow, increment row
                column = 0
                row += 1  # Increment the row if columns overflow
                # Reset bank and bank group to zero since row is incremented
                bank = 0
                bank_group = 0

            # Create the address by placing the bits in the right positions
            address = (row << (bank_bits + bank_group_bits + 10 + offset_bits)) | \
                      (bank_group << (bank_bits + 10 + offset_bits)) | \
                      (bank << (10 + offset_bits)) | \
                      (column << offset_bits)  # Column occupies 10 bits

            # Write to the trace file
            formatted_address = f"0x{address:08X}"  # Format with zero-padding to 8 hex digits
            f.write(f"{formatted_address} {read_or_write}\n")

            # Increment column for the next write
            column += 1
    return filename


def create_trace_sequential_rows(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}_r.trace"

    max_rows = (1 << 16)  # 10 bits for columns, i.e., 1024
    row_bits = 16
    bank_bits = 2
    bank_group_bits = 1
    offset_bits = 3

    # Counters for the fields in the address
    row = 0
    bank_group = 0
    bank = 0
    column = 0

    with open(filename, 'w') as f:
        for i in range(num_writes):
            if row >= max_rows:  # Column overflow, increment row
                column += 1
                row = 0  # Increment the row if columns overflow
                # Reset bank and bank group to zero since row is incremented
                bank = 0
                bank_group = 0

            # Create the address by placing the bits in the right positions
            address = (row << (bank_bits + bank_group_bits + 10 + offset_bits)) | \
                      (bank_group << (bank_bits + 10 + offset_bits)) | \
                      (bank << (10 + offset_bits)) | \
                      (column << offset_bits)  # Column occupies 10 bits

            # Write to the trace file
            formatted_address = f"0x{address:08X}"  # Format with zero-padding to 8 hex digits
            f.write(f"{formatted_address} {read_or_write}\n")

            # Increment column for the next write
            row += 1
    return filename


def create_trace_sequential_banks(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}_b.trace"

    max_columns = (1 << 10)  # 10 bits for columns, i.e., 1024
    max_banks = 4  # 2 bits for banks, i.e., 4 banks
    max_bank_groups = 2  # 1 bit for bank group, i.e., 2 bank groups
    row_bits = 16
    bank_bits = 2
    bank_group_bits = 1
    offset_bits = 3

    # Counters for the fields in the address
    row = 0
    column = 0
    bank_index = 0  # We will interleave between 8 banks (4 banks * 2 bank groups)

    with open(filename, 'w') as f:
        for i in range(num_writes):
            # Determine the bank group and bank based on bank_index (to interleave)
            bank_group = (bank_index >> bank_bits) & 0x1  # 1 bit for bank group
            bank = bank_index & 0x3  # 2 bits for banks

            # Create the address by placing the bits in the right positions
            address = (row << (bank_bits + bank_group_bits + 10 + offset_bits)) | \
                      (bank_group << (bank_bits + 10 + offset_bits)) | \
                      (bank << (10 + offset_bits)) | \
                      (column << offset_bits)  # Column occupies 10 bits

            # Write to the trace file
            formatted_address = f"0x{address:08X}"  # Format with zero-padding to 8 hex digits
            f.write(f"{formatted_address} {read_or_write}\n")

            # Increment the bank index to interleave across banks
            bank_index += 1

            # Once we've cycled through all 8 banks, reset the bank index and increment the column
            if bank_index >= (max_banks * max_bank_groups):  # 8 banks in total
                bank_index = 0
                column += 1  # Move to the next column after all banks are used

            # If the column overflows, reset column and increment row
            if column >= max_columns:
                column = 0
                row += 1  # Increment the row when columns overflow

    return filename



def create_trace_sequential_columns_interleaved(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}_ci.trace"

    max_columns = (1 << 10)  # 10 bits for columns, i.e., 1024
    row_bits = 16
    bank_bits = 2
    bank_group_bits = 1
    offset_bits = 3

    # Counters for the fields in the address
    row = 0
    bank_group = 0
    bank = 0
    column = 0

    with open(filename, 'w') as f:
        for i in range(num_writes):
            if column >= max_columns:  # Column overflow, increment row
                column = 0
                row += 1  # Increment the row if columns overflow
                # Reset bank and bank group to zero since row is incremented
                bank = 0
                bank_group = 0

            # Create the address by placing the bits in the right positions
            address = (row << (bank_bits + bank_group_bits + 10 + offset_bits)) | \
                      (bank_group << (bank_bits + 10 + offset_bits)) | \
                      (bank << (10 + offset_bits)) | \
                      (column << offset_bits)  # Column occupies 10 bits

            # Write to the trace file
            formatted_address = f"0x{address:08X}"  # Format with zero-padding to 8 hex digits
            f.write(f"{formatted_address} W\n")
            f.write(f"{formatted_address} R\n")

            # Increment column for the next write
            column += 1
    return filename


def create_trace_sequential_rows_interleaved(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}_ri.trace"

    max_rows = (1 << 16)  # 10 bits for columns, i.e., 1024
    row_bits = 16
    bank_bits = 2
    bank_group_bits = 1
    offset_bits = 3

    # Counters for the fields in the address
    row = 0
    bank_group = 0
    bank = 0
    column = 0

    with open(filename, 'w') as f:
        for i in range(num_writes):
            if row >= max_rows:  # Column overflow, increment row
                column += 1
                row = 0  # Increment the row if columns overflow
                # Reset bank and bank group to zero since row is incremented
                bank = 0
                bank_group = 0

            # Create the address by placing the bits in the right positions
            address = (row << (bank_bits + bank_group_bits + 10 + offset_bits)) | \
                      (bank_group << (bank_bits + 10 + offset_bits)) | \
                      (bank << (10 + offset_bits)) | \
                      (column << offset_bits)  # Column occupies 10 bits

            # Write to the trace file
            formatted_address = f"0x{address:08X}"  # Format with zero-padding to 8 hex digits
            f.write(f"{formatted_address} W\n")
            f.write(f"{formatted_address} R\n")

            # Increment column for the next write
            row += 1
    return filename


def create_trace_sequential_banks_interleaved(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}_bi.trace"

    max_columns = (1 << 10)  # 10 bits for columns, i.e., 1024
    max_banks = 4  # 2 bits for banks, i.e., 4 banks
    max_bank_groups = 2  # 1 bit for bank group, i.e., 2 bank groups
    row_bits = 16
    bank_bits = 2
    bank_group_bits = 1
    offset_bits = 3

    # Counters for the fields in the address
    row = 0
    column = 0
    bank_index = 0  # We will interleave between 8 banks (4 banks * 2 bank groups)

    with open(filename, 'w') as f:
        for i in range(num_writes):
            # Determine the bank group and bank based on bank_index (to interleave)
            bank_group = (bank_index >> bank_bits) & 0x1  # 1 bit for bank group
            bank = bank_index & 0x3  # 2 bits for banks

            # Create the address by placing the bits in the right positions
            address = (row << (bank_bits + bank_group_bits + 10 + offset_bits)) | \
                      (bank_group << (bank_bits + 10 + offset_bits)) | \
                      (bank << (10 + offset_bits)) | \
                      (column << offset_bits)  # Column occupies 10 bits

            # Write to the trace file
            formatted_address = f"0x{address:08X}"  # Format with zero-padding to 8 hex digits
            f.write(f"{formatted_address} W\n")
            f.write(f"{formatted_address} R\n")

            # Increment the bank index to interleave across banks
            bank_index += 1

            # Once we've cycled through all 8 banks, reset the bank index and increment the column
            if bank_index >= (max_banks * max_bank_groups):  # 8 banks in total
                bank_index = 0
                column += 1  # Move to the next column after all banks are used

            # If the column overflows, reset column and increment row
            if column >= max_columns:
                column = 0
                row += 1  # Increment the row when columns overflow

    return filename





def run_ramulator(size, filename):
    stats_file = "DDR4.stats"
    # Command to run the Ramulator simulator
    command = ["./ramulator", "../configs/DDR4-config.cfg", "--mode=dram", filename]  # Adjust the command and path as necessary
    try:
        # Run the command and wait for it to finish
        subprocess.run(command, check=True)
        print(f"Ran Ramulator for trace file {filename}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Ramulator: {e}")
        
    return stats_file


def read_stats(stats_file, lines):
    dram_cycles = None
    try:
        with open(stats_file, 'r') as f:
            for line in f:
                if lines in line:  
                    parts = line.split()
                    if len(parts) > 1:  
                        dram_cycles = float(parts[1])  # Extract the value as float
                        break
                    else:
                        print("Line format unexpected, no value found.")
    except FileNotFoundError:
        print(f"{stats_file} not found.")
    except ValueError as e:
        print(f"Error converting value to float: {e}")
    
    if dram_cycles is None:
        print("Could not find ramulator.dram_cycles in the stats file.")
    
    return dram_cycles

def process_scenario(size, writes, scenario,results,lines,operation):
        if scenario == 'columns':
            filename = create_trace_sequential_columns(size, writes, "W")
        elif scenario == 'rows':
            filename = create_trace_sequential_rows(size, writes, "W")
        elif scenario == 'banks':
            filename = create_trace_sequential_banks(size, writes, "W")
        else:
            raise ValueError("Invalid scenario")
        stats_file = run_ramulator(size, filename)
        
        if operation:
            op1 = read_stats(stats_file, lines[0])
           
            
            result= op1/size

            results.append(result)
        else:
            op1 = read_stats(stats_file, lines[0])
            results.append(op1)
        
    
def main():
    sizes = [
        512/2,
        512,     # 0.5 KB
        1024,    # 1 KB
        2048,    # 2 KB
        4096,    # 4 KB
        8192,    # 8 KB
        16384,   # 16 KB
        32768,   # 32 KB
        65536,   # 64 KB
        131072,  # 128 KB
        262144  # 256 KB
        #524288,  # 512 KB
    ]
    
    lines = [
        "ramulator.dram_cycles",
        "ramulator.average_serving_requests_0",
    ]
    
    title = "DRAM cycles per byte"
    y_label = "DRAM cycles per byte"
    operation=True
    
    columns= []
    rows= []
    banks= []
    
    num_writes = [int(size * 0.5) for size in sizes]  # Set the number of writes you want for each size
    



    for size, writes in zip(sizes, num_writes):
        process_scenario(size, writes, 'columns',columns,lines,operation)
        process_scenario(size, writes, 'rows',rows,lines,operation)
        process_scenario(size, writes, 'banks',banks,lines,operation)
    
   
    
    
    plot_comparison(sizes, columns, rows, banks, y_label,title)   
    plot_graph(sizes, banks, "DRAM cycles per byte", "DRAM cycles per byte (banks)")
    plot_graph(sizes, columns, "DRAM cycles per byte", "DRAM cycles per byte (columns)")
    
    plt.show()


def plot_graph(sizes, dram_cycles_list, ylabel, title):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, dram_cycles_list, marker='o', linestyle='-', color='b')
    plt.title(title)  # Updated title
    plt.xlabel('Trace File Size (Bytes)')
    plt.xscale('log', base=2)  # Set x-axis to logarithmic scale
    size_labels = ['256', '512', '1K', '2K', '4K', '8K', '16K', '32K', '64K', '128K', '256K']
    plt.xticks(sizes, size_labels)
    plt.ylabel(ylabel)  # Optional: update ylabel as well
    plt.grid(True)
    
    
def plot_comparison(sizes, dram_cycles_columns,dram_cycles_rows, dram_cycles_banks, ylabel,title):
    plt.figure(figsize=(10, 6))

    # Plot for each scenario
    plt.plot(sizes, dram_cycles_columns, marker='o', linestyle='-', color='b', label='Sequential Columns')
    plt.plot(sizes, dram_cycles_banks, marker='^', linestyle='-', color='g', label='Sequential Banks')
    plt.plot(sizes, dram_cycles_rows, marker='s', linestyle='-', color='r', label='Sequential Rows')
    plt.title(title)
    plt.xlabel('Trace File Size (Bytes)')
    plt.xscale('log', base=2)
    size_labels = ['256', '512', '1K', '2K', '4K', '8K', '16K', '32K', '64K', '128K', '256K']
    plt.xticks(sizes, size_labels)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()  # Show the legend to differentiate scenarios
    

if __name__ == "__main__":
    main()


