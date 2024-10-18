import os
import subprocess
import matplotlib.pyplot as plt

def create_trace_sequential_columns(size, num_writes, read_or_write):
    filename = f"trace_{size}_bytes_{read_or_write}.trace"

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
    filename = f"trace_{size}_bytes_{read_or_write}.trace"

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
    filename = f"trace_{size}_bytes_{read_or_write}.trace"

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
    filename = f"trace_{size}_bytes_{read_or_write}.trace"

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
    filename = f"trace_{size}_bytes_{read_or_write}.trace"

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
    filename = f"trace_{size}_bytes_{read_or_write}.trace"

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

def process_scenario(size, writes, scenario,metrics,results):
        if scenario == 'columns':
            filename = create_trace_sequential_columns_interleaved(size, writes, "W")
        elif scenario == 'rows':
            filename = create_trace_sequential_rows_interleaved(size, writes, "W")
        elif scenario == 'banks':
            filename = create_trace_sequential_banks_interleaved(size, writes, "W")
        else:
            raise ValueError("Invalid scenario")
        stats_file = run_ramulator(size, filename)
        for key, line in metrics.items():
            if key == "incoming_requests_per_channel / ramulator.active_cycles_0":
                # Read both incoming_requests_per_channel and active_cycles_0
                incoming_requests = read_stats(stats_file, metrics["incoming_requests_per_channel"])
                active_cycles = read_stats(stats_file, metrics["active_cycles_0"])
                
                
                # Ensure active_cycles is not zero to avoid division by zero
                if active_cycles and active_cycles != 0:
                    result = incoming_requests / active_cycles
                else:
                    result = 0  # Assign 0 if active cycles is zero
                    
                results[key][scenario].append(result)
            elif key == "transaction_bytes_to_bandwidth_ratio":
                
                read_bytes = read_stats(stats_file, metrics["read_transaction_bytes_0"])
                write_bytes = read_stats(stats_file, metrics["write_transaction_bytes_0"])
                max_bandwidth = read_stats(stats_file, metrics["maximum_bandwidth"])
                
                # Ensure max_bandwidth is not zero to avoid division by zero
                if max_bandwidth and max_bandwidth != 0:
                    total_bytes = read_bytes + write_bytes
                    result = total_bytes / max_bandwidth
                else:
                    result = 0  # Assign 0 if max_bandwidth is zero
                
                # Store the result in the dictionary
                results[key][scenario].append(result)
            elif key=="cycles/active cyles":
                cycle= read_stats(stats_file, metrics["dram_cycles"])    
                active= read_stats(stats_file, metrics["active_cycles_0"])    
                
                result= cycle/active
                results[key][scenario].append(result)
            elif key=="dram_cycles / ramulator.dram_capacity":
                cycle= read_stats(stats_file, metrics["dram_cycles"])    
                active= size   
                
                result= cycle/active
                results[key][scenario].append(result)
                print(1)
            else:
                results[key][scenario].append(read_stats(stats_file, line))

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
        "ramulator.row_misses_channel_0_core", 
        "ramulator.read_latency_avg_0", #
        "ramulator.in_queue_req_num_avg",
        "ramulator.in_queue_read_req_num_avg",
        "ramulator.in_queue_write_req_num_avg",
        "ramulator.write_row_hits_channel_0_core",
        "ramulator.write_row_misses_channel_0_core",
        "ramulator.write_row_conflicts_channel_0_core",
        "ramulator.serving_requests_0",
        "ramulator.read_row_conflicts_channel_0_core",
        "ramulator.write_row_conflicts_channel_0_core",
        "ramulator.req_queue_length_sum_0", 
        "ramulator.in_queue_req_num_sum",
        "ramulator.incoming_requests_per_channel",
        "ramulator.active_cycles_0", #
        "ramulator.maximum_bandwidth", #
        "ramulator.write_transaction_bytes_0",
        "ramulator.read_transaction_bytes_0",
        "ramulator.dram_capacity"
        
    ]
    
    num_writes = [int(size * 0.5) for size in sizes]  # Set the number of writes you want for each size
    
    metrics = {
        "average_serving_requests": lines[1],
        "ramulator.serving_requests_0":lines[10],
        "dram_cycles": lines[0],
        "row_misses": lines[2],
        "ramulator.read_row_conflicts_channel_0_core": lines[11],
        "ramulator.write_row_conflicts_channel_0_core": lines[12],
        "read_latency_avg": lines[3],
        "in_queue_req_num_avg": lines[4],
        "in_queue_read_req_num_avg": lines[5],
        "in_queue_write_req_num_avg": lines[6],
        "write_row_hits":lines[7],
        "write_row_misses": lines[8],
        "write_row_conflicts": lines[9],
        "ramulator.req_queue_length_sum_0": lines[13],
        "ramulator.in_queue_req_num_sum": lines[14],
        "incoming_requests_per_channel": lines[15],
        "active_cycles_0": lines[16],
        "incoming_requests_per_channel / ramulator.active_cycles_0": lines[16],
        "maximum_bandwidth": lines[17],
        "write_transaction_bytes_0": lines[18],
        "read_transaction_bytes_0": lines[19],
        "transaction_bytes_to_bandwidth_ratio": lines[19],
        "cycles/active cyles":lines[0],
        "dram_capacity": lines[20],
        "dram_cycles / ramulator.dram_capacity": lines[20]
    }
    
    results = {key: {'columns': [], 'rows': [], 'banks': []} for key in metrics}


    for size, writes in zip(sizes, num_writes):
        for scenario in ['columns', 'rows', 'banks']:
            process_scenario(size, writes, scenario,metrics,results)
    
    titles = {
        "average_serving_requests": ("Average Serving Requests per Memory Cycle", "DDR4 - Average Serving Requests"),
        "ramulator.serving_requests_0": ("Total Serving Requests per Memory Cycle", "DDR4 - Total Serving Requests"),
        "dram_cycles": ("Number of Cycles", "DDR4 - Number of Cycles"),
        "row_misses": ("Number of Row Misses", "DDR4 - Row Misses"),
        "ramulator.read_row_conflicts_channel_0_core": ("Read Row Conflicts", "DDR4 - Read Row Conflicts"),
        "ramulator.write_row_conflicts_channel_0_core": ("Write Row Conflicts", "DDR4 - Write Row Conflicts"),
        "read_latency_avg": ("Average Read Latency (Cycles)", "DDR4 - Average Read Latency"),
        "in_queue_req_num_avg": ("Average In-Queue Requests", "DDR4 - Average In-Queue Requests"),
        "in_queue_read_req_num_avg": ("Average In-Queue Read Requests", "DDR4 - Average In-Queue Read Requests"),
        "in_queue_write_req_num_avg": ("Average In-Queue Write Requests", "DDR4 - Average In-Queue Write Requests"),
        "write_row_hits": ("Write Row Hits", "DDR4 - Write Row Hits"),
        "write_row_misses": ("Write Row Misses", "DDR4 - Write Row Misses"),
        "write_row_conflicts": ("Write Row Conflicts", "DDR4 - Write Row Conflicts"),
        "ramulator.req_queue_length_sum_0": ("Request Queue Length", "DDR4 - Request Queue Length"),
        "ramulator.in_queue_req_num_sum": ("Total In-Queue Requests", "DDR4 - Total In-Queue Requests"),
        "incoming_requests_per_channel": ("Incoming Requests per Channel", "DDR4 - Incoming Requests per Channel"),
        "active_cycles_0": ("Active Cycles", "DDR4 - Active Cycles"),
        "incoming_requests_per_channel / ramulator.active_cycles_0": ("Number of requests per active cycle", "DDR4 - Requests per active cycle"),
        "maximum_bandwidth": ("Maximum Bandwidth (Bytes)", "DDR4 - Maximum Bandwidth"),
        "write_transaction_bytes_0": ("Write Transaction Bytes", "DDR4 - Write Transaction Bytes"),
        "read_transaction_bytes_0": ("Read Transaction Bytes", "DDR4 - Read Transaction Bytes"),
        "transaction_bytes_to_bandwidth_ratio": ("Transaction Bytes to Bandwidth Ratio", "DDR4 - Transaction Bytes to Bandwidth Ratio"),
        "cycles/active cyles": ("Cycles to Active Cycles", "DDR4 - Cycles to Active Cycles"),
        "dram_capacity": ("dram_capacity", "DDR4 - dram_capacity"),
        "dram_cycles / ramulator.dram_capacity": ("DRAM cycles per byte", "DRAM cycles per byte")
    }
    """
    for key in metrics:
        y_label, plot_title = titles[key]  # Unpack y-axis label and plot title
        plot_comparison(sizes,
                        results[key]['columns'],
                        results[key]['rows'],
                        results[key]['banks'],
                        y_label,    # Use y-axis label
                        plot_title)  # Use plot title
    """
    key="dram_cycles / ramulator.dram_capacity"
    y_label, plot_title = titles[key]  # Unpack y-axis label and plot title
    plot_comparison(sizes,
                    results[key]['columns'],
                    results[key]['rows'],
                    results[key]['banks'],
                    y_label,    # Use y-axis label
                    plot_title)  # Use plot title
    #plot_graph(sizes, results["dram_cycles / ramulator.dram_capacity"]["banks"], "DRAM cycles per byte", "DRAM cycles per byte (banks)")
    #plot_graph(sizes, results["dram_cycles / ramulator.dram_capacity"]["columns"], "DRAM cycles per byte", "DRAM cycles per byte (columns)")
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


