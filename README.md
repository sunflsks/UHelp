## Inspiration
In a world that is supposed to be more connected than ever before, we are seeing higher and higher levels of isolation and mental illness. In environments where stress and anxiety are already present (college *cough cough*), people feel even less confident about accessing the mental health resources they need. To make sure students are actively accessing mental health resources, we developed UHelp.

## What it does
UHelp is an interactive website that utilizes fine-tuned Cohere LLMs to provide users with specific mental health resources on the UMass campus that address their immediate needs. From text input to image analysis, our website provides thorough mental health resources for UMass students.

## How we built it
After scraping over 4000 UMass-related web pages, we broke each page up into chunks that were ~500 tokens in length each and vectorized each chunk using a Cohere LLM in order to capture semantic meaning. We then stored each of these vectors (and their associated text chunks) in a vector database. For each query made by the user, we again used the same Cohere API to obtain an embedding, which was then compared with the other vectors in the vector database to find the 15 most similar vectors. The text chunks associated with these 15 vectors were then concatenated and fed into a separate Cohere API to provide context about resources that were most similar to what the user asked.

We then used OpenCV and Pytesseract, the Python wrapper for Google’s Tesseract-OCR Engine, to binarize images into two colors given a specific color threshold. Using OpenCV, we could then easily convert this image to a string and pass this into the same query system.

We then incorporated these technologies into a Flask framework that handled HTTP methods between the client and the server, then accessed the server of an old laptop that hosted our website https://uhelp.tech.

## Challenges we ran into

Our first challenge was ensuring that our LLM model could be specific to UMass students, while also not hallucinating. We overcame this challenge by fine tuning the Command R+ model on all of UMass’s mental health resources, and by using the preamble functionality that Cohere provides to adjust both the formatting and the accuracy of the information presented. 

Another challenge was bringing together the front-end and back-end to be able to use the Cohere API on our website. We utilized Flask to be able to make requests between the front-end and back-end. 

Our final challenge was optimizing the response time on the website. In order to get faster output from our LLM, we optimized our preamble function and fine tuning process, which meant the user had to wait less time for the output.


## Accomplishments that we're proud of
Everyone feels isolated at times, and we feel as if UHelp is a great future resource for UMass students to feel comfortable sharing their feelings and accessing their resources.

We are proud of our ability as freshmen to implement full-stack development, LLM fine-tuning, and image analysis into a comprehensive project. UMass students can use our interface to find appropriate resources and solutions on campus if they upload concerning images (eg. harmful text messages).

## What we learned
As a team of freshmen, we dove head-first into many, many challenges.

From reinforcing our questionable front-end skills to optimizing text analysis from images, we faced many challenges and learned the whole 9 yards.

We believe our biggest learning moment was Implementing image analysis through py-tesseract, as it was something none of us had done before and provided a skill that we can build upon in the future.

## What's next for UHelp
UHelp can be expanded to cover more mental health resources that are available at UMass. Moreover, this strategy of fine-tuning LLMs for specific needs and circumstances can be applied to other universities across the world.


Beyond mental health, our fine-tuning strategy could be applied to other departments or websites, where finding resources is crucial to the well-being of students, faculty or staff. For example, the W.E.B. Du Bois library offers many resources for tutoring, writing, and other academic support. However, many of these resources can be difficult to learn about or access. We would love to see the day where each department at UMass has a website that allows users to interact with fine-tuned large language models, allowing students, faculty and staff to access the resources and information they need.
