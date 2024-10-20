October 20 2024
Lehigh Valley Hackathon
Team 20. Ursinus College. Evan Tilton, Michael Connors

## AWS and AI Usage
We used AWS to host an EC2 instance. We downloaded from the github repository and use the EC2 as a virtual computing environment. 
Many college students don't have access to fast computers, so utilizing virtual computing can help them run resource heavy programs
such as this one.
We also used Amazon Titan to generate AI images to be used as inputs. This is a fun way of combining images. For instance, a selfie
can be combined with an AI generated image with vibrant colors.

## Submission: Image Plating
Python file for image mosaicing while preserving all color pixels. 
Basically, it maps the colors of one image ("color image") to the structure of another image ("form image"),

Most image mosaicing algorithms distort colors to produce a final image.
This approach preserves all pixels in the color image.

The output is an image that can still be understood as the form image but it's made out of variable size chunks
of the color image. Higher precision increases runtime but uses smaller and smaller chunks, meaning
more of the form image is retained. In the extreme case, every single pixel is individually mapped, creating
a perfectly intelligible output. In real world usage, the runtime increases exponentially with image resolution and
chosen precision. This is inherent to the program. For instance, the hungarian algorithm is used to solve the
balanced assignment problem. This is generally the most effective solution for the balanced assignment problem,
yet it is still O(n^3). Because of the limitations involved in directly mapping pixels, the app will likely
not be able to handle very high resolution images with high precision, even with many code improvements.
As such, it serves as more of a cool tool and thought exercise than a scalable app. 

## Challenges
My team hoped to write this in c++ for a linear speed improvement in the nested loops. 
But, we changed gears and continued working in python because there are many useful libraries,
notably the python scipy libary includes optimize.linear_sum_assignment(), which is in fact an implementation of 
the hungarian algorithm.
We don't consider this to be a tragedy, since writing it in c++ would not have changed the fact that the time complexity is exponential.



