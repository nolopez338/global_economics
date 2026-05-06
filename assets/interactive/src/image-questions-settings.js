window.InteractiveImageQuestionSettings = {
  imageQuestions: [
    {
      id: "image-question-1",
      title: "Identify the target region",
      prompt: "Draw over the requested region in the image.",
      imageUrl: "https://example.com/image.jpg",
      goalRegion: {
        type: "normalized-mask",
        width: 100,
        height: 100,
        filledCells: []
      },
      explanation: "Cover all required cells to be marked correct."
    }
  ]
};
