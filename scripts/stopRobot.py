from pymorse import Morse

def main():
    with Morse() as morse:
        motion1 = morse.robot1.motion
        motion2 = morse.robot2.motion
        v_w = {"v": 0, "w": 0}
        motion1.publish(v_w)
        motion2.publish(v_w)

        exit()

if __name__ =="__main__":
    main()
