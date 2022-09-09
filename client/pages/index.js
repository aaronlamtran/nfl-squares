import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import Axios from "Axios";

export default function Home({ homeData }) {
  return (
    <div className={styles.container}>
      <Head>
        <title>Check NFL Squares</title>
        {/* <link rel="icon" href="/favicon.ico" /> */}
      </Head>
      <h1>Check NFL Squares</h1>
      {homeData.map((game) => (
        <div>
          <div key={game.filename}>
            {game.filename}
            <div>{game.line_one_away}</div>
            <div>{game.line_two_home}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
export const getStaticProps = async () => {
  const data = await Axios.get("http://localhost:5001/try_this");
  return {
    props: {
      homeData: data.data,
    },
  };
};
