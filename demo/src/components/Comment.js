import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp } from "@fortawesome/free-regular-svg-icons";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
export default function Comment() {
  return (
    <div className="cmt-wrapper">
      <img src="./images/0-user-face.png" className="user-face"></img>
      <div className="info">
        <div className="cmt-header">
          <div className="user-info">
            <p className="user-id">我不是momo</p>
            <p className="is-op">楼主</p>
          </div>
          <div className="header-right">
            <p className="create-at">2022-11-26 北京</p>
            <FontAwesomeIcon icon={faEllipsis} className="dots-icon" />
          </div>
        </div>
        <div className="quote">
          <div className="quote-content">
            momo:
            男女队各自大循环。。。大循环后去积分前四的队伍进第二阶段。。。第二阶段两两淘汰制。。。
          </div>
          <div className="quote-img-container">
            <img className="quote-img" src="./images/0-quote-img.png"></img>
            <div className="quote-gif-badge">GIF</div>
          </div>
        </div>
        <div className="cmt-content">那少了好多乐子</div>
        <div className="cmt-img-container">
          <img src="./images/22-cmt.png" className="cmt-img"></img>
          <div className="cmt-gif-badge">GIF</div>
        </div>
        <div className="likes">
          <a className="like-icon">
            <FontAwesomeIcon icon={faThumbsUp} />
          </a>
          <p className="like-cnt">9</p>
        </div>
      </div>
    </div>
  );
}
