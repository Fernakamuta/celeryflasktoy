

example = {
  "questions": [
    {
      "question_id": "A",
      "text": "exampleA",
      "type": "radio-string",
      "answers": [
        {
          "answer_id": "A1",
          "text": "Discordo Totalmente",
          "score": -2
        },
        {
          "answer_id": "A2",
          "text": "Discordo",
          "score": -1
        },
        {
          "answer_id": "A3",
          "text": "Neutro",
          "score": 0
        },
        {
          "answer_id": "A4",
          "text": "Concordo",
          "score": 1
        },
        {
          "answer_id": "A5",
          "text": "Concordo Plenamente",
          "score": 2
        }
      ],
      "answered": None
    },
    {
      "id": "B",
      "text": "ExampleB",
      "type": "slide-number",
      "answers": [
        {
          "answer_id": "B0",
          "text": "Discordo Totalmente",
          "score": -2
        },
        {
          "answer_id": "B1",
          "text": "Discordo",
          "score": -1
        },
        {
          "answer_id": "B2",
          "text": "Neutro",
          "score": 0
        },
        {
          "answer_id": "B3",
          "text": "Concordo",
          "score": 1
        },
        {
          "answer_id": "B4",
          "text": "Concordo Plenamente",
          "score": 2
        }
      ],
      "answered": None
    }
  ]
}


class Sampler:
    def survey(self, metrics, historic):
        return example
