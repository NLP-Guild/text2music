# Text-to-Music Generation
This is the Github Repository for the project "Text-to-Music Generation".

- To have some intuition about how this works, check this huggingface space: https://huggingface.co/spaces/Mubert/Text-to-Music
- Currently, we are in a stage where we should check related work and communicate ideas. Later, once we have some creative ideas, we can make plans and start implementation.
- This is an open-source project, so you're welcome to come up with ideas at any time or directly contribute to the GitHub repository.

You're welcome to join our [discord server](https://discord.gg/GbpJrQuNdg) to share your thoughts and report feedbacks!


## Roadmap
- [ ] check related work
- [ ] make a plan/timeline
- [ ] start implementation

## Quick Start
> **Recommended Python Version: 3.7**
1. installation: 
      ```
      pip install text2music
      ```
2. experimental example:
      ```python
      import text2music as t2m
      t2m.experimental.mubert_generate(
        prompt = 'I am quite happy today',
        duration = 10,
        output_path = 'test.mp3'
    )
      ```



## Contribution
The easiest way to contribute is to check our [task list](https://github.com/orgs/NLP-Guild/projects/3) and see what you could help. Then, you can simply open a pull request to contribute the codes :)
- if you are new to GitHub pull request, check this [document](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

Or, if you have any novel ideas about text-to-music generation, feel free to discuss in the [discord server](https://discord.gg/GbpJrQuNdg):
<a href = "https://discord.gg/GbpJrQuNdg">
<img src = "https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" width = 2%></img>
</a>

We appreciate your contribution!

## Active Line of Work
1. we are collecting real user prompts for later dataset building. If you would like to share your ideas, fill this [google form](https://forms.gle/Fmp8aSU3f6ThmeaT9) and submit. We really appreciate your help and will add you to the "wall of love" later:)
2. We are currently building our website: https://nlp-guild.github.io/text2music/. You're welcome to contribute 🙂

Check more details [here](https://github.com/orgs/NLP-Guild/projects/3)




