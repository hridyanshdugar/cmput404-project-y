import '@fortawesome/fontawesome-svg-core/styles.css'
import style from './singlepost.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHome } from '@fortawesome/free-solid-svg-icons'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { faBell } from '@fortawesome/free-solid-svg-icons'
import { faPerson } from '@fortawesome/free-solid-svg-icons'
import { faEnvelope } from '@fortawesome/free-solid-svg-icons'
import { faPen } from '@fortawesome/free-solid-svg-icons'
import { faEllipsis } from '@fortawesome/free-solid-svg-icons'

type Props = {
    name: string;
    profileImage: string;
    username: string;
    text: string;
    postImage: string | undefined;
    date: number;
    likes: number;
    retweets: number;
    comments: number;
    postID: number;
};

export default function SinglePost(props: Props) {
    return <div>
        <div>{ props.profileImage }</div>
        <div>
            <div>
                <div>
                    {props.name}
                </div>
                <div>
                    {props.username}
                </div>
                <div>
                    {props.date}
                </div>
                <div>
                    icon
                </div>                   
            </div>
            <div>
                {props.text}
            </div>
            <div>
                {props.postImage}
            </div>
            <div>
                <div>
                    {props.comments}
                </div>
                <div>
                    {props.retweets}
                </div>
                <div>
                    {props.likes}
                </div>
                <div>
                    share {props.postID}
                </div>                   
            </div>            
        </div>
    </div>;
}
