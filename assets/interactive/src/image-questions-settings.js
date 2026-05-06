window.InteractiveImageQuestionSettings = {
  imageQuestions: [
    {
      id: "image-question-1",
      title: "Identify the target region",
      prompt: "Draw over the requested region in the image.",
      imageUrl: "https://example.com/image.jpg",
      studentInkPercent: 150,
      coverGoalPercent: 90,
      goalRegion: {
        type: "normalized-mask",
        width: 100,
        height: 100,
        filledCells: []
      },
      explanation: "Cover the required percentage of the goal region to be marked correct."
    }
  ]
};
