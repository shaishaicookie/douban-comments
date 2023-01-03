import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp } from "@fortawesome/free-regular-svg-icons";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
export default function Comment(props) {
  return (
    <div className="cmt-wrapper">
      <img src={`../images/${props.item.user_face}`} className="user-face" />
      <div className="info">
        <div className="cmt-header">
          <div className="user-info">
            <p className="user-id">{props.item.user_id}</p>
            {props.item.is_op && <p className="is-op">楼主</p>}
          </div>
          <div className="header-right">
            <p className="create-at">{props.item.create_at}</p>
            <FontAwesomeIcon icon={faEllipsis} className="dots-icon" />
          </div>
        </div>
        {props.item.quote.quote_status && (
          <div className="quote">
            <div className="quote-content">
              {props.item.quote.quote_user_id}: {props.item.quote.quote_content}
            </div>
            {props.item.quote.quote_img.quote_img_status && (
              <div className="quote-img-container">
                <img
                  className="quote-img"
                  src={`../images/${props.item.quote.quote_img.quote_img_src}`}
                />
                {props.item.quote.quote_img.is_gif && (
                  <div className="quote-gif-badge">GIF</div>
                )}
              </div>
            )}
          </div>
        )}
        <div className="cmt-content">{props.item.cmt.cmt_content}</div>
        {props.item.cmt.cmt_img.cmt_img_status && (
          <div className="cmt-img-container">
            <img
              src={`../images/${props.item.cmt.cmt_img.cmt_img_src}`}
              className="cmt-img"
            ></img>
            {props.item.cmt.cmt_img.is_gif && (
              <div className="cmt-gif-badge">GIF</div>
            )}
          </div>
        )}
        <div className="likes">
          <a className="like-icon">
            <FontAwesomeIcon icon={faThumbsUp} />
          </a>
          <p className="like-cnt">{props.item.like_cnt}</p>
        </div>
      </div>
    </div>
  );
}
