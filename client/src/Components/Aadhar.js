import React from "react";
import ReactDOM from "react-dom";
import ImageUploading from "react-images-uploading";
import axios from "axios";
import "./Aadhar.css";
import { Link } from "react-router-dom";


function Aadhar() {
  const[flag,setflag] = React.useState([]);
  const [data, setdata] = React.useState([]);
  const [images, setImages] = React.useState([]);
  const maxNumber = 69;
  const onChange = (imageList, addUpdateIndex) => {
    // data for submit
    console.log(imageList, addUpdateIndex);
    // console.log(imageList)
    setImages(imageList);
    console.log(images);
    axios
      .post("http://127.0.0.1:5000/aadhar", { data: imageList[0].data_url })
      .then((res) => {
        console.log(`response = ${res.data}`);
        setdata(res.data);
        setflag(true);
      })
      .catch((error) => {
        console.log(`error = ${error}`);
      });
  };

  return (
    <div className="Aadhar">
      <ImageUploading
        multiple
        value={images}
        onChange={onChange}
        maxNumber={maxNumber}
        dataURLKey="data_url"
      >
        {({
          imageList,
          onImageUpload,
          onImageRemoveAll,
          onImageUpdate,
          onImageRemove,
          isDragging,
          dragProps,
        }) => (
          // write your building UI
          <div>
          <div className="upload__image-wrapper">
            <button onClick={onImageUpload} {...dragProps}>
              Click or Drop here
            </button>
            &nbsp;
            {/* <button onClick={onImageRemoveAll}>Remove all images</button> */}
            {imageList.map((image, index) => (  
              <div key={index} className="image-item">
                <center>
                  <img
                    className="img-box"
                    src={image.data_url}
                    alt=""
                    width="100"
                  />
                </center>
                <h2>{data}</h2>
               {data && <Link to="/otp" className="btn btn-primary">Age token</Link>} 
                {console.log(image.data_url)}
              </div>
            ))}
            
            
            
            </div>
           
            
            
           
            
          </div>
        )}
      </ImageUploading>
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Aadhar />, rootElement);

export default Aadhar;
