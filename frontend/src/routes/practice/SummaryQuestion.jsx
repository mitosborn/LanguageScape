
export default function SummaryQuestion({question}) {
    const {sentence, choices, answer} = question
    let answerStart = sentence.indexOf(choices[answer])
    let answerEnd = answerStart + choices[answer].length
    let beforeAnswer = sentence.substring(0, answerStart)
    let afterAnswer = sentence.substring(answerEnd)

    return (
        <div className={"d-flex gap-2"}>
            <h4>{beforeAnswer}</h4>
            <h4 style={{backgroundColor: "#FFFF00"}}>{choices[answer]}</h4>
            <h4>{afterAnswer}</h4>
        </div>
    )
}