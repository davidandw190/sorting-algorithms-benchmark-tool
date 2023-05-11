def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    stack = [(0, len(arr) - 1)]

    while stack:
        left, right = stack.pop()

        if left >= right:
            continue

        pivot = arr[right]
        i = left - 1

        for j in range(left, right):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[right] = arr[right], arr[i + 1]

        stack.append((left, i))
        stack.append((i + 2, right))

    return arr


def heap_sort(arr):
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = int(arr[i] // exp)
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i-1]

    for i in range(n-1, -1, -1):
        index = int(arr[i] // exp)
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    max_value = max(arr)
    exp = 1
    while max_value // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr


def bucket_sort(arr):
    """
    Sorts a list of numbers using bucket sort.

    :param arr: List of numbers to be sorted.
    :return: Sorted list of numbers.
    """
    # Find the minimum and maximum values in the list
    min_value = int(min(arr))
    max_value = int(max(arr))

    # Determine the range of values and size of each bucket
    range_values = max_value - min_value + 1
    bucket_size = 10
    num_buckets = (range_values + bucket_size - 1) // bucket_size

    # Create empty buckets
    buckets = [[] for _ in range(num_buckets)]

    # Assign each element to a bucket based on its value
    for num in arr:
        bucket_index = int((num - min_value) // bucket_size)
        buckets[bucket_index].append(num)

    # Sort each bucket using insertion sort
    for i in range(num_buckets):
        buckets[i].sort()

    # Concatenate the sorted buckets
    sorted_arr = []
    if min_value < 0:
        sorted_arr += buckets[0]
        for i in range(1, num_buckets):
            sorted_arr += buckets[i]
    else:
        for bucket in buckets:
            sorted_arr += bucket

    return sorted_arr


def tim_sort(arr):
    return sorted(arr)
