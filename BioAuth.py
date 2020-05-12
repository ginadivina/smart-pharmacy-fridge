import face_recognition
import cv2
import numpy as np
import threading



def main():
	# Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    videoThread = threading.Thread(target = captureVideo, args=(video_capture, ))
    videoThread.start()
    videoThread.join();
    video_capture.release()
    cv2.destroyAllWindows()

def captureVideo(video_capture):
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    last_face_encoding = [0]*128
    consecutivelyFound = 0

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
		
		    #What is no faces are found
        
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces([last_face_encoding], face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    #first_match_index = matches.index(True)
                    consecutivelyFound = consecutivelyFound + 1
                else:
                    consecutivelyFound = 0
                    face_names = []

                face_names.append(name)
                last_face_encoding = face_encoding
            if (len(face_encodings) == 0):
                consecutivelyFound = 0
        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
        #    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4#

        #    # Draw a box around the face
        #    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #    # Draw a label with a name below the face
            if consecutivelyFound >=5:
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "Face Identified", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        #    else:
        #        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #        font = cv2.FONT_HERSHEY_DUPLEX
        #        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return


if __name__ == "__main__":
    main()
