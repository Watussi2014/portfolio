import random
import sys
import pandas as pd


class Dice:

    """
    Dice class that simulate a dice.
    Initiate with a specific number of faces.
    Roll methods that generate a random number depending on the number of faces.
    """

    def __init__(self, faces: int) -> None:
        if faces > 100 or faces <= 0:
            raise ValueError("Incorrect number of faces.")
        else:
            self.faces = faces

    def roll(self):
        return random.randint(1, self.faces)


class Dice_cup:

    """
    Class that simulate a cup with 1-5 dices.

    Attributes:

    dice_num -> int, number of dices in the cup.
    dice_list -> list containing dice objects.
    throw_num -> int, number of times the throw_dices method has been used.
    roll_df -> Pandas Dataframe containing all the data about the rolls.
    last_throw -> Pandas dataframe containing all the data about the last roll.
    """

    def __init__(self) -> None:
        self.dice_num = 0
        self.dice_list = []
        self.throw_num = 0
        self.roll_df = pd.DataFrame(columns=["Throw", "Faces", "Roll"])
        self.last_throw = pd.DataFrame(columns=["Throw", "Faces", "Roll"])

    def add_dice(self, faces: int) -> None:
        """
        Generate a new dice with n faces and add it to the list.
        """
        if self.dice_num >= 5:
            raise ValueError("Dice cup already full")
        else:
            self.dice_num += 1
            dice = Dice(faces)
            self.dice_list.append(dice)

    def reset_dice(self) -> None:
        self.dice_num = 0
        self.dice_list = []

    def reset_last(self) -> None:
        self.last_throw = pd.DataFrame(columns=["Throw", "Faces", "Roll"])

    def throw_dices(self) -> None:
        """
        Roll the dices inside the cup and put the result in the roll and last throw dataframe.
        """
        self.throw_num += 1
        self.reset_last()

        for dice in self.dice_list:
            results = {}
            results["Throw"] = self.throw_num
            results["Faces"] = dice.faces
            results["Roll"] = dice.roll()

            self.roll_df = pd.concat(
                [self.roll_df, pd.DataFrame([results])], ignore_index=True
            )
            self.last_throw = pd.concat(
                [self.last_throw, pd.DataFrame([results])], ignore_index=True
            )

    def print_last(self) -> None:
        print("Here is the information about the last throw :")
        print(self.last_throw)

    def print_all_throws(self) -> None:
        print("Here is the information about all the throws that the cup has made :")
        print(self.roll_df.tail(100))

    def print_cup_info(self) -> None:
        print(f"The cup contains {self.dice_num} dice(s).")
        for dice in self.dice_list:
            print(f"A dice with {dice.faces} faces.")
        print("\n")


def cup_setup(list_faces=[]) -> Dice_cup:
    """
    Setup the number of dices and faces for the roll.
    Return a dice_cup instance.
    """
    number_of_dices = len(list_faces)

    if number_of_dices == 0:  # Manual setup of the cup
        number_of_dices = int(input("How many dices do you want ? "))
        if number_of_dices > 5 or number_of_dices < 1:
            raise ValueError("Incorrect value of dices")
        else:
            cup = Dice_cup()
            for i in range(number_of_dices):
                faces = int(input(f"How many faces for dice number {i+1} ? "))
                cup.add_dice(faces)

    else:
        cup = Dice_cup()
        for face in list_faces:
            cup.add_dice(face)

    return cup


def cup_update(cup: Dice_cup) -> None:
    """
    Remove all the dices from a cup and ask for new dices.
    """
    cup.reset_dice()

    number_of_dices = int(input("How many dices do you want ? "))
    if number_of_dices > 5 or number_of_dices < 1:
        raise ValueError("Incorrect value of dices")
    else:
        for i in range(number_of_dices):
            faces = int(input(f"How many faces for dice number {i+1} ? "))
            cup.add_dice(faces)


def menu(cup: Dice_cup) -> None:
    user_input = int(
        input(
            "What do you want to do ? \n 1. Throw the dice \n 2. See the rolls \n 3. Change the dices \n 4. See cup informations \n 5. Exit \n : "
        )
    )

    if user_input == 1:
        cup.throw_dices()
        cup.print_last()

    elif user_input == 2:
        cup.print_all_throws()

    elif user_input == 3:
        cup_update(cup)

    elif user_input == 4:
        cup.print_cup_info()

    elif user_input == 5:
        sys.exit()

    else:
        print("Unrecognized command")


def main():
    faces = [int(face) for face in sys.argv[1:]]  # Get the faces numbers from argv

    if len(faces) > 0:
        cup = cup_setup(faces)
    else:
        cup = cup_setup()  # If no argv, setup the cup manually

    cup.print_cup_info()
    while True:
        menu(cup)


if __name__ == "__main__":
    main()
