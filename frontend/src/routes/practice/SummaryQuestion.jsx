
export default function SummaryQuestion({question}) {
    const {original_text, choices, answer} = question
    let answerStart = original_text.indexOf(choices[answer])
    let answerEnd = answerStart + choices[answer].length
    let beforeAnswer = original_text.substring(0, answerStart)
    let afterAnswer = original_text.substring(answerEnd)

    return (
        <div className={"d-flex gap-2"}>
            <h4>{beforeAnswer}</h4>
            <h4 style={{backgroundColor: "#FFFF00"}}>{choices[answer]}</h4>
            <h4>{afterAnswer}</h4>
        </div>
    )
}