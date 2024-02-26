import '@fortawesome/fontawesome-svg-core/styles.css'
import style from './rightbar.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHome } from '@fortawesome/free-solid-svg-icons'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { faBell } from '@fortawesome/free-solid-svg-icons'
import { faPerson } from '@fortawesome/free-solid-svg-icons'
import { faEnvelope } from '@fortawesome/free-solid-svg-icons'
import { faPen } from '@fortawesome/free-solid-svg-icons'
import { faEllipsis } from '@fortawesome/free-solid-svg-icons'
import { Card, Form } from 'react-bootstrap'


export default function Rightbar() {
    return <>
        <div className={"main"}>
            <div className={style.borderContainer}>
            <nav className={style.rightnav}>
                                <Form.Control
                        type="text"
                        placeholder="Search"
                        className={["mr-sm-2", style.bottomMargin].join(' ')}
                        />       
                <Card className={style.bottomMargin}>
      <Card.Body>This is some text within a card body.</Card.Body>
                </Card>
                <Card className={style.bottomMargin}>
      <Card.Body>This is some text within a card body.</Card.Body>
                </Card>
                <Card className={style.bottomMargin}>
      <Card.Body>This is some text within a card body.</Card.Body>
    </Card>
            </nav>   
            </div>            
        </div>
    </>;
}
