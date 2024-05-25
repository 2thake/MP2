import numpy as np
import matplotlib.pyplot as plt
import cv2
from planet import place_planet
from io import BytesIO

def animate(storage, planets):

    frame_size = (1920, 1080)  # Width and height of the video
    # Read background image
    background_image = cv2.imread('pexels-francesco-ungaro-998641.jpg')

    # Create a figure and axis for the plot
    fig = plt.figure(figsize=[19.2, 10.8])
    ax = fig.add_subplot(111, projection='3d')

    # OpenCV VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    fps = 60  # Frames per second

    out = cv2.VideoWriter('SolarSystemFixed.mp4', fourcc, fps, frame_size)
    num_frames = storage.shape[1]

    # Define the initial camera angles
    # initial_elev = 0  # Initial elevation angle
    # final_elev = 30  # Initial elevation angle
    # initial_azim = 0   # Initial azimuth angle
    # final_azim = 160   # Final azimuth angle to complete a full rotation
    # elev_step = (final_elev - initial_elev) / num_frames  # Calculate the step size for azimuth angle
    # azim_step = (final_azim - initial_azim) / num_frames  # Calculate the step size for azimuth angle

    sun = planets[0]
    #Initial Value Problem
    for j, planet in enumerate(planets):
       if planet == sun:
           continue
       for i in range(0, num_frames):
            planet.path.append(storage[0+3*(j-1):3+3*(j-1), i])
    
    # Loop to create frames
    for N in range(num_frames):
        ax.clear()
        for planet in planets:
            if planet == sun:
                continue
                # planet.position = planet.position + (planet.velocity * sun_values.reshape((-1,1)))
            planet.position = planet.path[N]

        max_orbit = max(np.linalg.norm(planet.position) for planet in planets)
        # max_orbit = 30

        ax.axis('off')
        ax.set_box_aspect([1,1,1])
        ax.set_xlim(-max_orbit, max_orbit)
        ax.set_ylim(-max_orbit, max_orbit)
        ax.set_zlim(-max_orbit, max_orbit)
        ax.set_facecolor((1, 1, 1, 0))  # Set axis background to be completely transparent

        for planet in planets:
            place_planet(planet.radius, planet.texture, ax, planet.position, 60)
            if planet == sun:
                continue
            path = np.array(planet.path)
            transpose = np.transpose(path[:N])
            ax.plot(*transpose)
        
        # # Update the camera view angle
        # current_azim = initial_azim + N * azim_step
        # current_elev = initial_elev + N * elev_step
        # ax.view_init(elev=current_elev, azim=current_azim)

        # Save the plot as a PNG with a transparent background
        fig.savefig('temp_frameFixed.png', transparent=True)

        frame_with_transparency = cv2.imread('temp_frameFixed.png', cv2.IMREAD_UNCHANGED)
        frame_with_transparency = cv2.resize(frame_with_transparency, frame_size)

        resized_background = cv2.resize(background_image, frame_size)

        # Split the image into BGR and Alpha channels
        bgr = frame_with_transparency[:, :, :3]
        alpha = frame_with_transparency[:, :, 3]

        # Create an alpha mask
        alpha_mask = alpha / 255.0
        alpha_inv = 1.0 - alpha_mask

        # Blend the background with the BGR image using the alpha mask
        for c in range(0, 3):
            resized_background[:, :, c] = (alpha_mask * bgr[:, :, c] +
                                           alpha_inv * resized_background[:, :, c])

        # Write the frame to the video
        out.write(resized_background)

    # Release the video writer
    out.release()
        
    plt.close(fig)

    print("Video has been written successfully.")
