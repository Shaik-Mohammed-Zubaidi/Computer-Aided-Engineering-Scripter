import React from 'react';
import './App.css';
import { Flex, Layout } from 'antd';
import MainPage from './MainPage';


const { Header, Content } = Layout;

const headerStyle = {
  textAlign: 'center',
  color: '#000000',
  height: 64,
  paddingInline: 48,
  lineHeight: '64px',
  backgroundColor: '#00FA9A',
  fontSize: 24,
};
const contentStyle = {
  textAlign: 'center',
  // minHeight: 120,
  height: '90vh',
  // lineHeight: '120px',
  // color: '#fff',
  // backgroundColor: '#0958d9',
};
// const siderStyle = {
//   textAlign: 'center',
//   lineHeight: '120px',
//   color: '#fff',
//   backgroundColor: '#1677ff',
// };
const App = () => (
  <Flex gap="middle" wrap>
    <Layout >
      <Header style={headerStyle} > Abaqus Scripting Agent</Header>
      <Content style={contentStyle}>
        <MainPage />
      </Content>
    </Layout>
  </Flex>
);
export default App;