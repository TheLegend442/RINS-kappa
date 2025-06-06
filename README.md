# RINS-kappa
Our RINS repository -> for all labs and our own robot :)



#### Requirements:

<pre lang="markdown">pip install sounddevice pynput openai-whisper speechrecognition vosk deepface scikit-image</pre>

<h2><i>Task_2s - all together</i></h2>

<pre lang="markdown">ros2 topic hz /oakd/rgb/preview/depth/points</pre>
<pre lang="markdown">ros2 topic hz "/top_camera/rgb/preview/depth/points"</pre>
<pre lang="markdown">ros2 launch task_2s task_2s_launch.py</pre>
<pre lang="markdown">ros2 run task_2s robot_commander.py</pre>
<pre lang="markdown">ros2 run task_2s speech_server.py</pre>

<h2><i>Task_2s - 'bridge_follower.py'</i></h2> 
<br>Python node that follows the bridge from starting point <i>'workspace/src/task_2s/data/bridge_start.npy'</i> to the red cross at the end of the world.

#### Running:

<pre lang="markdown">ros2 launch task_2s rviz_gazebo.launch.py</pre>
<pre lang="markdown">ros2 run dis_tutorial7 arm_mover_actions.py</pre>
<pre lang="markdown">ros2 topic pub --once /arm_command std_msgs/msg/String "{data: 'manual:[0.,0.,0.4,2.19]'}"</pre>
<pre lang="markdown">ros2 run task_2s robot_commander.py</pre>
<pre lang="markdown">ros2 run task_2s bridge_follower.py</pre>

<h2>Task_2s - ring, face and bird detction:</h2>

#### Face detection:
<pre lang="markdown">ros2 run task_2s detect_people.py</pre>
<pre lang="markdown">ros2 run task_2s save_faces.py</pre>

#### Ring detection:
<pre lang="markdown">ros2 topic pub --once /arm_command std_msgs/msg/String "{data: 'manual:[0.,0.0,0.5,1.0]'}"</pre>
<pre lang="markdown">ros2 run task_2s detect_rings_final.py</pre>
<pre lang="markdown">ros2 run task_2s save_rings.py</pre>

#### Bird detection:
<pre lang="markdown">ros2 run task_2s detect_birds.py</pre>
<pre lang="markdown">ros2 run task_2s save_birds.py</pre>

<h2>Task_2s - Bird Catalogue</h2>
<p><i>'bird_catalogue_server.py'</i> is a service server that takes <i>'BirdCollection.srv'</i> as an input which is a list of <i>'Bird.msg'</i> messages, and forms a PDF catalogue 'RINS-KAPPA/bird_catalogue.pdf'. As a example of it's work there is service client <i>bird_client_example.py</i></p>

#### Running the example
<pre lang="markdown">ros2 run task_2s bird_catalogue_server.py</pre>
<pre lang="markdown">ros2 run task_2s bird_client_example.py</pre>

<h2>Task_2s - Dialogue</h2>

#### Requirements
<pre lang="markdown">sudo apt update
sudo apt install libportaudio2 portaudio19-dev ffmpeg</pre>
<pre lang="markdown">pip install sounddevice pynput openai-whisper speechrecognition vosk</pre>
