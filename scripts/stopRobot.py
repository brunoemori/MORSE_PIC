from pymorse import Morse

def main():
    with Morse() as morse:
        motion = morse.robot1.motion
        v_w = {"v": 0, "w": 0}
        motion.publish(v_w)
        exit()

if __name__ =="__main__":
    main()
