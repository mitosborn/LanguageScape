import {Link, Outlet, useLoaderData, useNavigation, useSubmit} from "react-router-dom";
import styled from 'styled-components'
import {Button, Col, Row} from "react-bootstrap";
import Container from "react-bootstrap/Container";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheckCircle, faPlayCircle } from '@fortawesome/fontawesome-free-solid'

const Li = styled.li`
  color : blue;
  font-size : 23px;
  border-radius: 25px;
  background-color: red;
  padding: 5px;
  margin: 20px;

  
`
const Ul = styled.ul`
  border : 2px solid green;
  width: 100%;
  list-style-type:none
`

const LearnSetCard = styled.div`
    border-radius: 15px;
    background-color: pink;
    padding: 20px;
    margin-bottom: 20px;
    font-size: 1px;
    @media screen and (min-width: 600px) {
        max-width: 65%;
    };
    
    @media screen and (max-width: 599px) {
        max-width: 90%;
    };
`

const TitleRow = styled.div`
    background-color: blue;
    font-weight: bold;
    text-align: center;
    font-size: 2.4rem;
`

const DescriptionRow = styled.div`
    background-color: yellow;
    font-weight: bold;
    font-size: 1.4rem;
`

const ProgressColumn = styled.div`
    font-size: 1.5rem;
    font-weight: bold;
    background-color: red;
    display: flex;
    justify-content: center;
    align-items: center;
`

const PlayColumn = styled.div`
    font-size: 1rem;
    font-weight: bold;
    background-color: purple;
    display: flex;
    justify-content: center;
    align-items: center;
`

const PlayButton = styled.div`
    font-size: 1rem;
    font-weight: bold;
    width: 100%;
    margin: 5px;
`
export default function LearnSet({learnSet}) {
    console.log(JSON.stringify(learnSet))
    const {name, id, numCompleted, totalNumber, description} = learnSet

    return (
        <LearnSetCard as={Container} className={"panel-body"}>
            <TitleRow as={Row}>
                <span>{name}</span>
            </TitleRow>
            <DescriptionRow as={Row}>
                <span>{description}</span>
            </DescriptionRow>
            <Row>
                <ProgressColumn as={Col} xs={12} sm={12} md={6} lg={5} xl={5} xxl={5}>
                    <div>
                        <FontAwesomeIcon style={{color: "yellow"}} icon={faPlayCircle} /> Played 0 <span className="hidden-xs">sentences </span>(0%)
                    </div>
                </ProgressColumn>
                <ProgressColumn as={Col} xs={12} sm={12} md={6} lg={5} xl={5} xxl={5} style={{fontSize: "1.5rem"}}>
                    <div>
                        <FontAwesomeIcon style={{color: "green"}} icon={faCheckCircle} /> Mastered {numCompleted} <span className="hidden-xs">sentences </span>(0%)
                    </div>
                </ProgressColumn>
            {/*</Row>*/}
            {/*<Row>*/}
                <PlayColumn as={Col} xs={12} sm={12} md={12} lg={2} xl={2} xxl={2}>
                    <PlayButton as={Link} to="/mc/20%20German%20Sentences/lsid/50/10" className={"btn btn-success btn-lg btn-block joystix visible-xs"}>
                        <FontAwesomeIcon icon="fa-solid fa-play" /> Play
                    </PlayButton>
                </PlayColumn>
            </Row>

        </LearnSetCard>
        // <div>
        //     <Ul>
        //         <Li>
        //             {JSON.stringify(learnSet)}
        //         </Li>
        //         <Li>
        //             {JSON.stringify(learnSet)}
        //         </Li>
        //     </Ul>
        // </div>
    );
}
