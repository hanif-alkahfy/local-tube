import { useState, useEffect } from 'react';
import Header from "../components/Header";
import VideoGrid from "../components/VideoGrid";

function Home() {
    const [videos, setVideos] = useState([]);

    useEffect(() => {
      const fetchVideos = async () => {
        try {
          const response = await fetch("http://localhost:5000/api/videos");
          const data = await response.json();
          setVideos(data.videos);
        } catch (error) {
          console.error("Gagal mengambil daftar video:", error);
        }
      };

      fetchVideos();
    }, []);

  return (
    <div className="h-screen">
      <Header />
      <VideoGrid videos={videos} />
    </div>
  );
}

export default Home;
