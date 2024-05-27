import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import time

# Create the main application window
root = tk.Tk()
root.title("Knapsack Problem Solver")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
style.configure("TEntry", font=("Helvetica", 12), padding=5)

# Frame for input fields
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)
# Title label
title_label = ttk.Label(
    input_frame, text="Knapsack Problem Solver", font=("Helvetica", 16, "bold")
)
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Value entry
values_label = ttk.Label(input_frame, text="Values (comma-separated):")
values_label.grid(row=1, column=0, sticky="e")
values_entry = ttk.Entry(input_frame)
values_entry.grid(row=1, column=1, padx=5)

# Weight entry
weights_label = ttk.Label(input_frame, text="Weights (comma-separated):")
weights_label.grid(row=2, column=0, sticky="e")
weights_entry = ttk.Entry(input_frame)
weights_entry.grid(row=2, column=1, padx=5)

# Capacity entry
capacity_label = ttk.Label(input_frame, text="Knapsack Capacity:")
capacity_label.grid(row=3, column=0, sticky="e")
capacity_entry = ttk.Entry(input_frame)
capacity_entry.grid(row=3, column=1, padx=5)

# Sliders label
slider_label = ttk.Label(root, text="Select Plot:")
slider_label.pack()

# Slider
slider = tk.Scale(root, from_=1, to=4, orient=tk.HORIZONTAL, length=200, bg="#f0f0f0")
slider.pack()

# Message for slider buttons
slider_message = ttk.Label(
    root,
    text="1) Greedy  2) Brute  3) DP  4) All combined",
    font=("Helvetica", 10),
    foreground="#404040",
)
slider_message.pack()

# Plot frame
plot_frame = tk.Frame(root, bg="#f0f0f0")
plot_frame.pack(pady=10)


def greedy_knapsack(values, capacity, weights):  #
    list_length = len(values)  # Get the length of the values list
    vpw = []  # Value Per Weight
    for i in range(list_length):  # A for loop that iterates over the list length
        ratio = values[i] / weights[i]  # Calculate the ratio for each item
        ipi = [ratio, i]  # Info Per Item; store the ratio and index
        vpw.append(ipi)  # Append the info per item to the vpw list

    vpw.sort(reverse=True)  # Sort the value per weight list in descending order

    total_value = 0  # Initialize total_value
    total_weight = 0  # Initialize total_weight
    final_knapsack = (
        []
    )  # Initialize list to store the selected items and their fractions

    for ratio, i in vpw:  # For loop iterates over each ratio and index in vpw
        if (
            total_weight + weights[i] <= capacity
        ):  # If adding the whole item stays within capacity
            final_knapsack.append(
                (i, 1)
            )  # Append the item index and fraction 1 (whole item)
            total_value += values[
                i
            ]  # Increase total_value by the value of the whole item
            total_weight += weights[
                i
            ]  # Increase total_weight by the weight of the whole item
        else:
            fraction = (capacity - total_weight) / weights[
                i
            ]  # Calculate the fraction of the item that can be added
            total_value += (
                values[i] * fraction
            )  # Increase total_value by the value of the fraction of the item
            total_weight += (
                weights[i] * fraction
            )  # Increase total_weight by the weight سof the fraction of the item
            final_knapsack.append(
                (i, fraction)
            )  # Append the item index and the fraction
            break  # The knapsack is now full

    return (
        final_knapsack,
        total_value,
        total_weight,
    )  # Return the final knapsack, total_value, total_weight


def knapsack_bruteforce(items, max_weight):
    def best_value(index, remaining_weight):
        if (
            index == len(items) or remaining_weight <= 0
        ):  # Base case: no more items or weight capacity
            return (0, [])

        weight, value = items[index]  # Get the weight and value of the current item

        if (
            weight > remaining_weight
        ):  # If the item's weight exceeds remaining capacity, skip the item
            return best_value(index + 1, remaining_weight)
        without_item = best_value(
            index + 1, remaining_weight
        )  # Recursive call without including the current item
        with_item = best_value(
            index + 1, remaining_weight - weight
        )  # Recursive call including the current item
        with_item = (
            with_item[0] + value,
            [index] + with_item[1],
        )  # Update the with_item value and list

        if (
            with_item[0] > without_item[0]
        ):  # Compare the values of including and excluding the item
            return with_item
        else:
            return without_item

    max_value, selected_items = best_value(
        0, max_weight
    )  # Get the maximum value and selected items
    total_weight = sum(
        items[i][0] for i in selected_items
    )  # Calculate the total weight of selected items
    return (
        selected_items,
        max_value,
        total_weight,
    )  # Return the selected items, max value, and total weight


def knapsack_dynamic(values, weights, capacity):
    n = len(values)  # Number of items

    if n != len(weights):  # Check if the number of values and weights are equal
        raise ValueError("Number of values and weights must be equal")

    if capacity <= 0:  # Check if the capacity is greater than zero
        raise ValueError("Knapsack capacity must be greater than zero")

    dp = [
        [0] * (capacity + 1) for _ in range(n + 1)
    ]  # 2D list to store the maximum value

    for i in range(1, n + 1):  # Iterate over each item
        for w in range(1, capacity + 1):  # Iterate over each capacity
            if (
                weights[i - 1] <= w
            ):  # Check if the item's weight is less than or equal to current capacity
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]
                )  # Maximize the value
            else:
                dp[i][w] = dp[i - 1][
                    w
                ]  # If item cannot be included, carry forward the value

    selected_items = []  # List to store the selected items
    total_weight = capacity  # Start with the total capacity
    for i in range(n, 0, -1):  # Backtrack to find the selected items
        if (
            dp[i][total_weight] != dp[i - 1][total_weight]
        ):  # Check if the item was included
            selected_items.append(i - 1)  # Add the item to the selected list
            total_weight -= weights[i - 1]  # Reduce the total weight

    max_value = dp[n][capacity]  # The maximum value that can be obtained

    return (
        selected_items[::-1],
        max_value,
        capacity - total_weight,
    )  # Return the selected items, max value, and total weight used


def Take_inputs():
    try:
        # Split the input by commas and convert to integers
        values = [int(x) for x in values_entry.get().split(",")]
        weights = [int(x) for x in weights_entry.get().split(",")]
        capacity = int(capacity_entry.get())

        # Check if the number of values and weights are equal
        if len(values) != len(weights):
            raise ValueError("The number of values must match the number of weights.")

        # Check if capacity is a positive integer
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        return values, weights, capacity

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
        return None, None, None


def run_algorithm():
    try:
        # Take inputs from the entry fields
        values, weights, capacity = Take_inputs()

        # Run the selected knapsack algorithm
        selected_algorithm = slider.get()
        if selected_algorithm == 1:
            selected_items, selected_value, selected_weight = greedy_knapsack(
                values, capacity, weights
            )
            algorithm_name = "Greedy"
        elif selected_algorithm == 2:
            items = list(zip(weights, values))
            selected_items, selected_value, selected_weight = knapsack_bruteforce(
                items, capacity
            )
            algorithm_name = "Brute Force"
        elif selected_algorithm == 3:
            selected_items, selected_value, selected_weight = knapsack_dynamic(
                values, weights, capacity
            )
            algorithm_name = "Dynamic Programming"
        elif selected_algorithm == 4:
            # Run all three algorithms and display combined outputs
            greedy_items, greedy_value, greedy_weight = greedy_knapsack(
                values, capacity, weights
            )
            brute_items, brute_value, brute_weight = knapsack_bruteforce(
                list(zip(weights, values)), capacity
            )
            dynamic_items, dynamic_value, dynamic_weight = knapsack_dynamic(
                values, weights, capacity
            )

            result_label.config(
                text=f"Greedy: Items: {greedy_items}, Value: {greedy_value}, Weight: {greedy_weight}\n"
                f"Brute Force: selected_items: {brute_items}, max_value: {brute_value}, max_weight: {brute_weight}\n"
                f"Dynamic: Items: {dynamic_items}, Value: {dynamic_value}, Weight: {dynamic_weight}"
            )
            return
        else:
            messagebox.showerror("Selection Error", "Invalid selection.")
            return

        # Update the result label with the results of the selected algorithm
        result_label.config(
            text=f"{algorithm_name}: Items: {selected_items}, Value: {selected_value}, Weight: {selected_weight}"
        )

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


def clear_entries():
    # Function to clear entry fields
    values_entry.delete(0, tk.END)
    weights_entry.delete(0, tk.END)
    capacity_entry.delete(0, tk.END)
    result_label.config(text="")


def plot():
    values, weights, capacity = Take_inputs()

    if values is None or weights is None or capacity is None:
        return  # Stop execution if input values are invalid

    try:
        capacities = list(range(1, capacity + 1))
        greedy_times = []
        brute_times = []
        dynamic_times = []

        greedy_values = []
        brute_values = []
        dynamic_values = []

        for c in capacities:
            start_time = time.time()
            _, greedy_value, _ = greedy_knapsack(values, c, weights)
            greedy_times.append(time.time() - start_time)
            greedy_values.append(greedy_value)

            start_time = time.time()
            _, brute_value, _ = knapsack_bruteforce(list(zip(weights, values)), c)
            brute_times.append(time.time() - start_time)
            brute_values.append(brute_value)

            start_time = time.time()
            _, dynamic_value, _ = knapsack_dynamic(values, weights, c)
            dynamic_times.append(time.time() - start_time)
            dynamic_values.append(dynamic_value)

        # Plot Greedy algorithm
        if slider.get() == 1:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            ax1.plot(capacities, greedy_times, label="Time (seconds)", color="blue")
            ax2.plot(capacities, greedy_values, label="Value", color="green")

            ax1.set_xlabel("Capacity")
            ax1.set_ylabel("Time (seconds)", color="blue")
            ax2.set_ylabel("Value", color="green")

            plt.title("Greedy Knapsack Algorithm")
            fig.legend(loc="upper left")
            plt.show()

        # Plot Brute Force algorithm
        elif slider.get() == 2:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            ax1.plot(capacities, brute_times, label="Time (seconds)", color="blue")
            ax2.plot(capacities, brute_values, label="Value", color="green")

            ax1.set_xlabel("Capacity")
            ax1.set_ylabel("Time (seconds)", color="blue")
            ax2.set_ylabel("Value", color="green")

            plt.title("Brute Force Knapsack Algorithm")
            fig.legend(loc="upper left")
            plt.show()

        # Plot Dynamic Programming algorithm
        elif slider.get() == 3:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()

            ax1.plot(capacities, dynamic_times, label="Time (seconds)", color="blue")
            ax2.plot(capacities, dynamic_values, label="Value", color="green")

            ax1.set_xlabel("Capacity")
            ax1.set_ylabel("Time (seconds)", color="blue")
            ax2.set_ylabel("Value", color="green")

            plt.title("Dynamic Programming Knapsack Algorithm")
            fig.legend(loc="upper left")
            plt.show()

        # Plot all three algorithms combined
        elif slider.get() == 4:
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

            ax1.plot(capacities, greedy_times, label="Greedy Time", color="blue")
            ax1.plot(capacities, brute_times, label="Brute Force Time", color="red")
            ax1.plot(capacities, dynamic_times, label="Dynamic Time", color="green")
            ax1.set_ylabel("Time (seconds)")
            ax1.legend(loc="upper left")

            ax2.plot(capacities, greedy_values, label="Greedy Value", color="blue")
            ax2.plot(capacities, brute_values, label="Brute Force Value", color="red")
            ax2.plot(capacities, dynamic_values, label="Dynamic Value", color="green")
            ax2.set_xlabel("Capacity")
            ax2.set_ylabel("Value")
            ax2.legend(loc="upper left")

            plt.title("Knapsack Algorithms Comparison")
            plt.show()

        else:
            messagebox.showerror("Selection Error", "Invalid selection.")

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


run_button = ttk.Button(root, text="Run Algorithm", command=run_algorithm)
run_button.pack(pady=5)

clear_button = ttk.Button(root, text="Clear Entries", command=clear_entries)
clear_button.pack(pady=5)

plot_button = ttk.Button(root, text="Plot", command=plot)
plot_button.pack(pady=5)

result_label = ttk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()
