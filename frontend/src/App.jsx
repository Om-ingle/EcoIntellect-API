import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Leaf, TrendingDown, Award, TreePine, ShoppingCart, CheckCircle, AlertTriangle, X, Bike } from 'lucide-react';

export default function EcoIntellectDashboard() {
  const [formData, setFormData] = useState({
    distance_km: 5,
    transport_mode: 'car',
    packaging_type: 'plastic',
    estimated_time_minutes: 30,
    order_value: 350,
    frequency_per_week: 3
  });

  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock Checkout State
  const [showCheckout, setShowCheckout] = useState(false);
  const [checkoutState, setCheckoutState] = useState('initial'); // 'initial', 'intercept', 'success'
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('https://ecointellect-api-production.up.railway.app/api/v1/analyze-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to analyze order. Make sure the Railway API is live and accessible.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 85) return 'bg-green-100';
    if (score >= 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-green-100">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-green-600 rounded-lg p-2">
                <Leaf className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">EcoIntellect</h1>
                <p className="text-sm text-gray-600">Sustainability Intelligence Layer</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Demo Dashboard</p>
              <p className="text-xs text-green-600 font-medium">Food Delivery Analysis</p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Panel - Input Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-800">Order Details</h2>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Distance (km)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData.distance_km}
                    onChange={(e) => setFormData({ ...formData, distance_km: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Transport Mode
                  </label>
                  <select
                    value={formData.transport_mode}
                    onChange={(e) => setFormData({ ...formData, transport_mode: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="car">Car</option>
                    <option value="motorcycle">Motorcycle</option>
                    <option value="electric_vehicle">Electric Vehicle</option>
                    <option value="bike">Bike</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Packaging Type
                  </label>
                  <select
                    value={formData.packaging_type}
                    onChange={(e) => setFormData({ ...formData, packaging_type: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="plastic">Plastic</option>
                    <option value="paper">Paper</option>
                    <option value="biodegradable">Biodegradable</option>
                    <option value="reusable">Reusable</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Order Value (₹)
                  </label>
                  <input
                    type="number"
                    value={formData.order_value}
                    onChange={(e) => setFormData({ ...formData, order_value: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Orders per Week
                  </label>
                  <input
                    type="number"
                    value={formData.frequency_per_week}
                    onChange={(e) => setFormData({ ...formData, frequency_per_week: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 transition-colors disabled:bg-gray-400"
                >
                  {loading ? 'Analyzing...' : 'Analyze Environmental Impact'}
                </button>

                <div className="relative flex items-center py-2">
                  <div className="flex-grow border-t border-gray-200"></div>
                  <span className="flex-shrink-0 mx-4 text-xs font-semibold text-gray-400 uppercase tracking-widest">or</span>
                  <div className="flex-grow border-t border-gray-200"></div>
                </div>

                <button
                  type="button"
                  onClick={() => setShowCheckout(true)}
                  className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors flex justify-center items-center shadow-lg shadow-gray-200"
                >
                  <ShoppingCart className="w-5 h-5 mr-2" />
                  Simulate Food App Checkout
                </button>
              </form>
            </div>
          </div>

          {/* Right Panel - Results */}
          <div className="lg:col-span-2">
            {!analysis ? (
              <div className="bg-white rounded-xl shadow-md p-12 text-center">
                <Leaf className="w-16 h-16 text-green-600 mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">Ready to Analyze</h3>
                <p className="text-gray-500">Enter order details and click analyze to see environmental impact</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Score Card */}
                <div className={`${getScoreBg(analysis.eco_score)} rounded-xl p-6 border-2 ${analysis.eco_score >= 85 ? 'border-green-300' : analysis.eco_score >= 70 ? 'border-yellow-300' : 'border-red-300'}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Eco Score</p>
                      <p className={`text-5xl font-bold ${getScoreColor(analysis.eco_score)}`}>
                        {analysis.eco_score}
                      </p>
                      <p className="text-lg font-medium text-gray-700 mt-1">{analysis.rating}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Carbon Emissions</p>
                      <p className="text-3xl font-bold text-gray-900">{analysis.carbon_emission_grams}g</p>
                      <p className="text-xs text-gray-500 mt-1">CO₂ per order</p>
                    </div>
                  </div>
                </div>

                {/* Alternatives List and Chart */}
                {analysis.better_alternatives.length > 0 && (
                  <div className="bg-white rounded-xl shadow-md p-6">
                    <h3 className="text-lg font-semibold mb-6 flex items-center">
                      <TrendingDown className="w-5 h-5 mr-2 text-green-600" />
                      CO₂ Emission Comparison
                    </h3>

                    <div className="h-64 mb-8">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={[
                            {
                              name: 'Your Choice',
                              emissions: analysis.carbon_emission_grams,
                            },
                            ...analysis.better_alternatives.map((alt) => ({
                              name: alt.transport_mode,
                              emissions: alt.carbon_emission_grams,
                            }))
                          ]}
                          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                          <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                          <YAxis axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 12 }} />
                          <Tooltip
                            cursor={{ fill: '#f3f4f6' }}
                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                          />
                          <Bar dataKey="emissions" radius={[6, 6, 0, 0]} barSize={40}>
                            {
                              [...Array(1 + analysis.better_alternatives.length)].map((_, index) => (
                                <Cell key={`cell-${index}`} fill={index === 0 ? '#ef4444' : '#10b981'} />
                              ))
                            }
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>

                    <h4 className="font-semibold text-gray-700 mb-3 text-sm uppercase tracking-wider">Top Eco-Friendly Options</h4>
                    <div className="space-y-3">
                      {analysis.better_alternatives.map((alt, idx) => (
                        <div key={idx} className="bg-green-50 border border-green-200 rounded-lg p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <p className="font-medium text-gray-900">
                                {alt.transport_mode} + {alt.packaging_type}
                              </p>
                              <p className="text-sm text-green-700 font-medium mt-1">
                                Save {alt.carbon_saved_grams}g CO₂
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="text-2xl font-bold text-green-600">{alt.eco_score}</p>
                              <p className="text-xs text-gray-600">Eco Score</p>
                            </div>
                          </div>
                          <div className="flex gap-4 text-sm text-gray-600">
                            <span>{alt.carbon_emission_grams}g CO₂</span>
                            <span>•</span>
                            <span>{alt.estimated_time_minutes} min</span>
                            <span>•</span>
                            <span>{alt.time_difference_minutes > 0 ? '+' : ''}{alt.time_difference_minutes} min diff</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Yearly Projection */}
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <TreePine className="w-5 h-5 mr-2 text-green-600" />
                    Your Year in Carbon
                  </h3>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-blue-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600">Total Orders</p>
                      <p className="text-3xl font-bold text-blue-600">{analysis.yearly_projection.total_orders_per_year}</p>
                    </div>
                    <div className="bg-orange-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600">Total Carbon</p>
                      <p className="text-3xl font-bold text-orange-600">{analysis.yearly_projection.total_carbon_kg} kg</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600">Trees to Offset</p>
                      <p className="text-3xl font-bold text-green-600">{analysis.yearly_projection.trees_needed_to_offset}</p>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4">
                      <p className="text-sm text-gray-600">Equiv. Car km</p>
                      <p className="text-3xl font-bold text-purple-600">{analysis.yearly_projection.equivalent_car_km.toFixed(0)}</p>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 mb-4">
                    <p className="text-sm text-gray-700">
                      <span className="font-medium">💡 Context:</span> {analysis.environmental_context}
                    </p>
                  </div>

                  {/* Wolfram Scale Scenarios */}
                  {analysis.yearly_projection.scale_scenarios && (
                    <div className="mt-4">
                      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1">
                        <span>📡</span> Wolfram|One Impact Simulation — If Users Switched to Eco-Delivery
                      </p>
                      <div className="h-48">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart
                            data={analysis.yearly_projection.scale_scenarios}
                            margin={{ top: 5, right: 10, left: -20, bottom: 0 }}
                          >
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                            <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 11 }} />
                            <YAxis axisLine={false} tickLine={false} tick={{ fill: '#6b7280', fontSize: 11 }} unit=" t" />
                            <Tooltip
                              cursor={{ fill: '#f0fdf4' }}
                              contentStyle={{ borderRadius: '10px', border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}
                              formatter={(val) => [`${val} tonnes CO₂`, 'CO₂ Saved']}
                            />
                            <Bar dataKey="total_co2_saved_tonnes" fill="#10b981" radius={[4, 4, 0, 0]} barSize={35} />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                      <p className="text-xs text-gray-400 text-center mt-2">CO₂ tonnes saved per year across user base</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer Note */}
        <div className="mt-8 text-center space-y-1">
          <p className="text-sm text-gray-600">
            🌍 EcoIntellect API • Sustainability Intelligence Layer for Food Delivery
          </p>
          <p className="text-xs text-gray-400">
            Powered by <span className="font-medium text-green-600">GreenPT</span> emission factors &amp; <span className="font-medium text-blue-600">Wolfram|One</span> impact modelling
          </p>
        </div>
      </div>

      {/* Mock Checkout Modal */}
      {showCheckout && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden relative">
            <button
              onClick={() => { setShowCheckout(false); setCheckoutState('initial'); }}
              className="absolute right-4 top-4 text-gray-400 hover:text-gray-600 z-10"
            >
              <X className="w-5 h-5" />
            </button>

            {checkoutState === 'initial' && (
              <div className="p-6">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Your Order</h2>
                  <p className="text-gray-500">Delicious Food Restaurant</p>
                </div>

                <div className="space-y-4 mb-6">
                  <div className="flex justify-between text-gray-700">
                    <span>1x Margherita Pizza</span>
                    <span>₹250</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span>1x Garlic Bread</span>
                    <span>₹100</span>
                  </div>
                  <div className="border-t pt-4 border-gray-200">
                    <div className="flex justify-between text-sm text-gray-500 mb-2">
                      <span>Delivery (<span className="capitalize">{formData.transport_mode.replace('_', ' ')}</span>)</span>
                      <span>₹40</span>
                    </div>
                    <div className="flex justify-between font-bold text-lg text-gray-900">
                      <span>Total</span>
                      <span>₹390</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setIsProcessing(true);
                    setTimeout(() => {
                      setIsProcessing(false);
                      setCheckoutState('intercept');
                    }, 1500);
                  }}
                  disabled={isProcessing}
                  className="w-full bg-orange-500 text-white py-4 rounded-xl font-bold text-lg hover:bg-orange-600 transition-colors flex justify-center items-center shadow-lg shadow-orange-200 relative overflow-hidden group"
                >
                  {isProcessing ? (
                    <span className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </span>
                  ) : (
                    <>
                      <span className="relative z-10 transition-transform group-hover:scale-105 duration-200">Proceed to Pay ₹390</span>
                      <div className="absolute inset-0 h-full w-full bg-white/20 scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300"></div>
                    </>
                  )}
                </button>
              </div>
            )}

            {checkoutState === 'intercept' && (
              <div className="p-6">
                <div className="bg-green-50 rounded-xl p-6 -mx-6 -mt-6 mb-6 border-b border-green-100 text-center relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-green-500"></div>
                  <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Leaf className="w-8 h-8 text-green-600" />
                  </div>
                  <h2 className="text-xl font-bold text-green-900 mb-2">EcoIntellect Suggestion!</h2>
                  <p className="text-green-800 text-sm px-2">
                    Did you know your current choice <span className="font-semibold">({formData.transport_mode.replace('_', ' ')} + {formData.packaging_type})</span> emits significant CO₂?
                  </p>
                </div>

                <div className="bg-white border-2 border-green-200 rounded-xl p-4 mb-6 shadow-sm">
                  <div className="flex items-start mb-3">
                    <Bike className="w-6 h-6 text-green-600 mr-3 mt-1" />
                    <div>
                      <h3 className="font-bold text-gray-900">Switch to Eco-Delivery</h3>
                      <p className="text-sm text-gray-600">Bike Delivery + Biodegradable Packaging</p>
                    </div>
                  </div>
                  <div className="bg-green-100 rounded-lg p-3 text-center border border-green-200">
                    <span className="font-bold text-green-800 block text-lg mb-1">Save ~320g of CO₂!</span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-200 text-green-800">
                      ₹10 Eco-Discount Applied
                    </span>
                  </div>
                </div>

                <div className="space-y-3">
                  <button
                    onClick={() => setCheckoutState('success')}
                    className="w-full bg-green-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-green-700 transition-all shadow-lg shadow-green-200 transform hover:-translate-y-1"
                  >
                    Accept Eco-Option & Pay ₹380
                  </button>
                  <button
                    onClick={() => setCheckoutState('success')}
                    className="w-full bg-gray-50 text-gray-600 py-3 rounded-xl font-medium hover:bg-gray-100 border border-gray-200 transition-colors"
                  >
                    Continue with Original Choice
                  </button>
                </div>
              </div>
            )}

            {checkoutState === 'success' && (
              <div className="p-8 text-center animate-in fade-in zoom-in duration-300">
                <div className="relative inline-block mb-6">
                  <div className="absolute inset-0 bg-green-100 rounded-full animate-ping opacity-75"></div>
                  <CheckCircle className="w-20 h-20 text-green-500 relative z-10 bg-white rounded-full" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Confirmed!</h2>
                <p className="text-gray-600 mb-8">
                  Your food is being prepared. Thank you for using EcoIntellect to make a difference! 🌍
                </p>
                <button
                  onClick={() => { setShowCheckout(false); setCheckoutState('initial'); }}
                  className="w-full bg-gray-900 text-white py-3 rounded-xl font-medium hover:bg-gray-800 transition-colors shadow-lg shadow-gray-200"
                >
                  Back to Dashboard
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}