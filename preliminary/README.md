<h1>Preliminary Tasks</h1>

<h3>1) Develop a program that takes video input and identifies objects in real time using a webcam</h3>
<p>The result can be seen at /Personcounter infer.py</p>
<ul>
    <li> We used roboflow to train a NN to detect people with boxes using the dataset given in /Personcounter/dataset</li>
    <ol>
        <li> It takes a 416x416 image as input</li>
        <li> Output is the same 416x416 image but with a box around any object detected as a person</li>
        <li> We used a split of 3778/412/14 for train/valid/test </li>
        <li> Trained over 44 epochs</li>
    </ol>
    <li> Our program uses openCV to get the current image for the chosen camera (laptop webcam in our case</li>
    <li> The image is resized to 416x416 maintaining aspect ratio</li>
    <li> The image is converted to a base 64 string</li>
    <li> Using a Roboflow API call we give the string (image) as input to our trained network</li>
    <li> We recieve the output image from the network, parse it, then display this again using openCV</li>
    <li> The result is a ≈ 4fps video that identifies any person in the webcam with a box and label "people"</li>
</ul>

<h3>2) Extend on the above by developing a program to count the number of people in a room</h3>

<ul>
<li> The training data used is shown under dataset 2</li>
<li> The same training process as above was used</li>
<li> The training started from mscoco object detection and previous people detection checkpoints for v1 and v2 respectively. V2 has marginally better performance.</li>
<li> In addition to the previous code, the response JSON is used to get the count of the number of predicitons.
This is printed as the count of the number of people in the video per frame.</li>
<li> Displaying image feed to user still occurs</li>
</ul>

<h3>3) Have this system work, standalone, on a rasberry pi with a camera</h3>
