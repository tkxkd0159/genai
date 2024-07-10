* Instead of sending a single string as your prompt, you send a list of messages as your input. 
* Each message in the list has two properties: role and content. 
  * The 'role' can take one of three values: 'system', 'user' or the 'assistant'
  * The 'content' contains the text of the message from the role. 
* The system instruction can give high level instructions for the conversation
* The messages are processed in the order they appear in the list, and the assistant responds accordingly.
  * Use `assistant` role to maintain the state of the conversation

# References
* [How to format inputs to ChatGPT models](https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models)