### 09/27/19
At this point, our team has most of the components to begin prototyping the product. We have a 1080p camera as well as at least one Raspberry Pi 3. The 4K camera has come in, but Dr. Higgins is holding on to it for now. We will also likely get a Raspberry Pi 4 since it has better processing power. At this point, our team has also reviewed the starter code that Paras has given us. Our next step is to get the starter code up and running (OpenCV and Flask properly installed).

### 10/01/19
Me, Bryce, Cole, and Shelby all met up at the library to go through the OpenCV install process together. This turned out to be a much more complicated task than we expected. It ended up taking us all around four hours to get all the OpenCV dependencies installed and built. We now have a basic video stream working though. [This](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) is the guide we used.

### 10/06/19
Added viewport functionality to our html index. This enables the video stream image to take up 100% of the viewport both vertically and horizontally. This will allow a better viewing fit for VR.

### 10/09/19
Today, we met with Paras at the eye clinic to get hands on exposure to a slit lamp microscope. This gave us a much better idea of what we are working this. Paras also had the 4K cameras in the microscopes so that we could see what a video stream of the slit lamp would look like.

### 10/25/19
Got external hosting working. Now, anyone who goes to the host's IP address will be able to see the video stream. This was accomplished by changing the Flask port to 80 as well as some router port forwarding configuration. [This](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/) is the guide I used to set up port forwarding on my home router. We also had a group call with Paras today where we laid out the next steps of the project. The next big goals will be more reliable streaming and some basic user interfacing.

### 10/30/19
Added an exit function that safely joins the CameraStream thread back to the parent to prevent a zombie process. This happens when a ctrl^c SIGINT is called. Basic resizing capability has also been added.

### 11/10/19
Created a `dual_stream.py`: a script that implements two threaded CameraStream objects and stitches the two images together to create a VR viewable image. It starts by prompting the user to input which camera sources to use. Then, it creates the camera objects. Finally, it continually streams the stitched images to an OpenCV window. Behind the scenes it is applying a crop function that takes the two images and fits them to a desired aspect ratio so that it fully fills up the VR headset's screen. It also has a zoom function that is determined based on a config .json file.

### 11/18/19
Wrote code that made sure that the OpenCV configuration settings were only updated whenever the config file *changed* as opposed to updating every single frame iteration. I also added code to flip the images vertically as well as swap the left and right side images.

### 11/20/19
Added FPS (frames per second) calculations for performance tests.
