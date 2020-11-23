import React from 'react';
import { Navigate } from 'react-router-dom';
import DashboardLayout from 'src/layouts/DashboardLayout';
// import MainLayout from 'src/layouts/MainLayout';
import HomePageView from 'src/views/HomePageView';
import NotFoundView from 'src/views/errors/NotFoundView';
import TempSensorView from 'src/views/TempSensorView';
import HeaterView from 'src/views/HeaterView';
import KettleView from 'src/views/KettleView';
import PumpView from 'src/views/PumpView';

const routes = [
  {
    path: '/',
    element: <DashboardLayout />,
    children: [
      { path: '', element: <HomePageView /> },
      { path: 'tempsensors', element: <TempSensorView /> },
      { path: 'heaters', element: <HeaterView /> },
      { path: 'kettles', element: <KettleView /> },
      { path: 'pumps', element: <PumpView /> },
      { path: '404', element: <NotFoundView /> },
      { path: '*', element: <Navigate to="/404" /> }
    ]
  }
];

export default routes;
