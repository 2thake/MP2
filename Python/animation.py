import numpy as np
import matplotlib.pyplot as plt
import cv2
from planet import place_planet
from matplotlib.colors import LightSource

def animate(storage, planets):
    # Read background image
    background_image = cv2.imread('pexels-francesco-ungaro-998641.jpg')

    # Create a figure and axis for the plot
    fig = plt.figure(figsize=[19.2, 10.8])
    ax = fig.add_subplot(111, projection='3d')

    # OpenCV VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    fps = 60  # Frames per second
    frame_size = (1920, 1080)  # Width and height of the video
    out = cv2.VideoWriter('SolarSystem1.mp4', fourcc, fps, frame_size)
    
    # Define the initial camera angles
    initial_elev = 10  # Initial elevation angle
    final_elev = 35  # Initial elevation angle
    initial_azim = 0   # Initial azimuth angle
    final_azim = 160   # Final azimuth angle to complete a full rotation
    num_frames = storage.shape[1]
    elev_step = (final_elev - initial_elev) / num_frames  # Calculate the step size for azimuth angle
    azim_step = (final_azim - initial_azim) / num_frames  # Calculate the step size for azimuth angle

    sun = planets[0]
    #Initial Value Problem
    for j, planet in enumerate(planets):
       if planet == sun:
           continue
       for i in range(0, num_frames):
            planet.path.append(storage[0+3*(j-1):3+3*(j-1), i])
    
    neptune = planets[-1]
    max_orbit = 0
    # Loop to create frames
    for N in range(num_frames):
        ax.clear()
        # ax.plot(x[:i], y[:i], 'b')
        # ax.set_xlim(-1.5, 1.5)
        # ax.set_ylim(-1.5, 1.5)
        # ax.set_title(f'Frame {i+1}/{len(theta)}')
        i = 0
        j = storage.shape[0]//2
        for planet in planets:
            if planet == sun:
                continue
                # planet.position = planet.position + (planet.velocity * sun_values.reshape((-1,1)))
            planet.position = planet.path[N]

        max_orbit = max(np.linalg.norm(planet.position) for planet in planets)
        # max_orbit = 0 #initialising max orbit to 0
        #This accounts for the maximum deviation from the centre of the planets orbits
        # for planet in planets: #iterating through all of the planets and calculating the euclidian distance, if this passes the max, set as new max
        #     d = np.linalg.norm(planet.position)
        #     if d > max_orbit:
        #         max_orbit = d

    
        # #Initial Value Problem
        # for k, planet in enumerate(planets):
        #     # for p in range(0, N+1):
        #     planet.path.append(storage[0+3*k:3+3*k, N])  
                # RungeKutta4_v1(planet, planets, h)
                # planet.position = EulersMethod(planet, planets, h)
        ax.axis('off')
        ax.set_box_aspect([1,1,1])
        ax.set_xlim(-max_orbit, max_orbit)
        ax.set_ylim(-max_orbit, max_orbit)
        ax.set_zlim(-max_orbit, max_orbit)

        for planet in planets:
            place_planet(planet.radius, planet.texture, ax, planet.position, 60)
            if planet == sun:
                continue
            path = np.array(planet.path)
            transpose = np.transpose(path[:N])
            ax.plot(*transpose)
        # for planet in planets:
        #     if len(planet.path) > 0:
        #         transpose = np.transpose(np.array(planet.path))
        #         ax.plot(transpose[0], transpose[1], transpose[2])
        #         place_planet(planet.radius, planet.texture, ax, planet.position, 60)
        
        # Update the camera view angle
        current_azim = initial_azim + N * azim_step
        current_elev = initial_elev + N * elev_step
        ax.view_init(elev=current_elev, azim=current_azim)

        # Save the plot as a PNG with a transparent background
        fig.savefig('temp_frame.png', transparent=True)

        # Read the saved PNG file
        frame_with_transparency = cv2.imread('temp_frame.png', cv2.IMREAD_UNCHANGED)
        # frame_with_transparency = cv2.resize(frame_with_transparency, frame_size)

        # Split the image into BGR and Alpha channels
        bgr = frame_with_transparency[:, :, :3]
        alpha = frame_with_transparency[:, :, 3]

        # Resize background image to match the size of the frame
        resized_background = cv2.resize(background_image, frame_size)

        # Create an alpha mask
        alpha_mask = alpha / 255.0
        alpha_inv = 1.0 - alpha_mask

        # Blend the background with the BGR image using the alpha mask
        for c in range(0, 3):
            resized_background[:, :, c] = (alpha_mask * bgr[:, :, c] +
                                           alpha_inv * resized_background[:, :, c])

        # Write the frame to the video
        out.write(resized_background)


        # Draw the canvas and convert to image
        # fig.canvas.draw()
        # img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        # img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # # Convert RGB to BGR for OpenCV
        # img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # # Resize background image to match the size of the frame
        # resized_background = cv2.resize(background_image, frame_size)

        # # Overlay animation on background image
        # combined_frame = resized_background.copy()
        # combined_frame[:img_bgr.shape[0], :img_bgr.shape[1]] = img_bgr


        # # Write frame to video
        # out.write(combined_frame)
        #     # Close the plot


    # Release the video writer
    out.release()
        
    plt.close(fig)


    print("Video has been written successfully.")
