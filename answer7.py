
def get_ec2_recommendation(instance_type, cpu_utilization):
    sizes = ["nano", "micro", "small", "medium", "large", "xlarge", "2xlarge",
             "4xlarge", "8xlarge", "16xlarge", "32xlarge"]

    
    parts = instance_type.split(".")
    if len(parts) != 2:
        print("Invalid instance type format.")
        return

    family, size = parts
    
    if size not in sizes:
        print("Unknown instance size.")
        return

    index = sizes.index(size)


    
    if cpu_utilization < 20 and index > 0:
        new_size = sizes[index - 1]  
        status = "Underutilized"
    elif cpu_utilization > 80 and index < len(sizes) - 1:
        new_size = sizes[index + 1]
        status = "Overutilized"
    else:
        new_size = size
        status = "Optimized"

    recommended_instance = f"{family}.{new_size}"

    print(f"{instance_type}        {cpu_utilization}             {status}      {recommended_instance}")

get_ec2_recommendation("t2.large", 81)