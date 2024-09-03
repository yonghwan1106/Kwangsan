import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { PieChart, Pie, Cell } from 'recharts';
import { MapPin, BarChart2, PieChart as PieChartIcon, Lightbulb } from 'lucide-react';

const data = [
  { district: '송정1동', carbonEmission: 120, energyEfficiency: 'B' },
  { district: '송정2동', carbonEmission: 150, energyEfficiency: 'C' },
  { district: '도산동', carbonEmission: 90, energyEfficiency: 'A' },
  { district: '신가동', carbonEmission: 200, energyEfficiency: 'D' },
  { district: '신창동', carbonEmission: 180, energyEfficiency: 'C' },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const CarbonFootprintApp = () => {
  const [activeTab, setActiveTab] = useState('map');
  const [selectedDistricts, setSelectedDistricts] = useState(data.map(d => d.district));

  const filteredData = data.filter(d => selectedDistricts.includes(d.district));

  const handleDistrictChange = (district) => {
    setSelectedDistricts(prev => 
      prev.includes(district) 
        ? prev.filter(d => d !== district)
        : [...prev, district]
    );
  };

  const renderContent = () => {
    switch(activeTab) {
      case 'map':
        return (
          <div className="bg-gray-200 p-4 rounded-lg">
            <p className="text-center">여기에 탄소발자국 지도가 표시됩니다.</p>
            <img src="/api/placeholder/400/300" alt="Map placeholder" className="mx-auto mt-4" />
          </div>
        );
      case 'chart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={filteredData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="district" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="carbonEmission" fill="#8884d8" name="탄소 배출량" />
            </BarChart>
          </ResponsiveContainer>
        );
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={filteredData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="carbonEmission"
                label={({ district, percent }) => `${district} ${(percent * 100).toFixed(0)}%`}
              >
                {filteredData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">광산구 탄소발자국 지도</h1>
      
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">지역 선택</h2>
        <div className="flex flex-wrap gap-2">
          {data.map(d => (
            <button
              key={d.district}
              onClick={() => handleDistrictChange(d.district)}
              className={`px-3 py-1 rounded ${
                selectedDistricts.includes(d.district)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              {d.district}
            </button>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <div className="flex border-b">
          <button
            className={`flex items-center px-4 py-2 ${activeTab === 'map' ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => setActiveTab('map')}
          >
            <MapPin className="mr-2" />
            지도
          </button>
          <button
            className={`flex items-center px-4 py-2 ${activeTab === 'chart' ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => setActiveTab('chart')}
          >
            <BarChart2 className="mr-2" />
            차트
          </button>
          <button
            className={`flex items-center px-4 py-2 ${activeTab === 'pie' ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => setActiveTab('pie')}
          >
            <PieChartIcon className="mr-2" />
            파이 차트
          </button>
        </div>
      </div>

      <div className="mb-4">
        {renderContent()}
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2 flex items-center">
          <Lightbulb className="mr-2" />
          탄소 저감 아이디어
        </h2>
        <ul className="list-disc pl-5">
          <li>대중교통 이용 장려 프로그램 도입</li>
          <li>건물 에너지 효율 개선 지원</li>
          <li>재생에너지 사용 확대</li>
          <li>녹지 공간 확충</li>
          <li>자전거 도로 확대</li>
        </ul>
      </div>
    </div>
  );
};

export default CarbonFootprintApp;
