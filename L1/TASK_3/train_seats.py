# Run: python L1/TASK_3/train_seats.py 3 25

import argparse

data = {
    1: [
        {"seat_name": "a1", "isTaken": True},
        {"seat_name": "a2", "isTaken": False},
        {"seat_name": "a3", "isTaken": True},
        {"seat_name": "a4", "isTaken": True},
        {"seat_name": "a5", "isTaken": False},
    ],
    2: [
        {"seat_name": "b1", "isTaken": False},
        {"seat_name": "b2", "isTaken": False},
        {"seat_name": "b3", "isTaken": True},
        {"seat_name": "b4", "isTaken": False},
        {"seat_name": "b5", "isTaken": True},
    ],
    3: [
        {"seat_name": "c1", "isTaken": False},
        {"seat_name": "c2", "isTaken": True},
        {"seat_name": "c3", "isTaken": True},
        {"seat_name": "c4", "isTaken": True},
        {"seat_name": "c5", "isTaken": False},
    ],
}


def nearest_free_seat(wagon_number, seat_index):
    seats = data[wagon_number]
    for distance in range(1, len(seats)):
        for index in (seat_index - distance, seat_index + distance):
            if 0 <= index < len(seats) and not seats[index]["isTaken"]:
                return wagon_number, seats[index]

    for other_number, other_seats in data.items():
        if other_number != wagon_number:
            for seat in other_seats:
                if not seat["isTaken"]:
                    return other_number, seat

    return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Check train seat availability by wagon and seat number."
    )
    parser.add_argument("wagon", type=int, help="Wagon number")
    parser.add_argument("seat", type=int, help="Seat number within the wagon (1-based)")
    args = parser.parse_args()

    if args.wagon not in data or not 0 <= args.seat - 1 < len(data[args.wagon]):
        print("ასეთი ვაგონი ან ადგილი არ არსებობს.")
        return

    seat_index = args.seat - 1
    seat = data[args.wagon][seat_index]

    if not seat["isTaken"]:
        print(f"ადგილი {seat['seat_name']} ვაგონში {args.wagon} თავისუფალია.")
        return

    print(f"ადგილი {seat['seat_name']} ვაგონში {args.wagon} დაკავებულია.")
    found_wagon, found_seat = nearest_free_seat(args.wagon, seat_index)
    if found_seat is not None:
        print(f"უახლოესი თავისუფალი ადგილი: {found_seat['seat_name']} (ვაგონი {found_wagon}).")
    else:
        print("მატარებელში თავისუფალი ადგილი არ არის.")


main()
