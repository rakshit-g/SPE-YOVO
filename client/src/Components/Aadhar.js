import React from "react";
import ReactDOM from "react-dom";
import ImageUploading from "react-images-uploading";
import axios from "axios";
import "./Aadhar.css";
import { Link   } from "react-router-dom";


function Aadhar() {
  const[flag,setflag] = React.useState([]);
  const [imageData, setImageData] = React.useState("");
  const [data, setdata] = React.useState([]);
  const [images, setImages] = React.useState([]);
  const maxNumber = 69;
  // const navigate = useNavigate();

  // const handleImageUpload = async (imageList) => {
  //   // Upload image and get the data URL
  //   const imageData = imageList[0].data_url;

  //   // Navigate to `/otp` route with the image data as state
  //   navigate("/otp", { state: { image: imageData } });
  // };
  const onChange = (imageList, addUpdateIndex) => {
    // data for submit
    console.log(imageList, addUpdateIndex);
    // console.log(imageList)
    setImages(imageList);

    // Navigate to `/otp` route with the image data as state
    
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
                {data.includes("Valid Aadhar Number") && (
                  <>
                    <p>If you want to save your age token to ease the process next time, click on the Age token:</p>
                    <Link
                      to={{
                        pathname: "/otp",
                        // state: { image: imageList[0].data_url }, // Pass the image data as state
                      }}
                      className="btn btn-primary"
                      // onClick={() => handleImageUpload([image])}
                    >
                      Age token
                    </Link>
                    <br />
                    <Link to="/" className="btn btn-primary">
                    You have verified your age this one time, go to store cart
                    </Link>
                  </>
                )}
                {/* {console.log(image.data_url)} */}
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
